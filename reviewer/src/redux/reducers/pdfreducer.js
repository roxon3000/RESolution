import {
    GET_TRENDS_INITIAL, GET_TRENDS_SUCCESS,
    GET_PTRENDS_INITIAL, GET_PTRENDS_SUCCESS,
    GET_HOME_INITIAL, GET_HOME_SUCCESS, GET_DPHRASE_SUCCESS
} from "../actionTypes";

const initialState = {
    home: {
        cards: [],
        data: []
    },
    trender: {
        trends: {
            top10: {}
        }
    },
    loading: false,
    trendsloading: false,
    charts: []
};

export default function (state = initialState, action) {
    switch (action.type) {
        case GET_HOME_INITIAL: {
            return {
                ...state,
                loading: true
            };
        }
        case GET_HOME_SUCCESS: {
            const serviceData = action.payload;
            return {
                ...state,
                home: serviceData,
                loading: false
            };
        }
        case GET_PTRENDS_INITIAL:
        case GET_TRENDS_INITIAL: {
            return {
                ...state,
                loading: true,
                trendsloading: true
            };
        }
        case GET_DPHRASE_SUCCESS:
        case GET_TRENDS_SUCCESS:
        case GET_PTRENDS_SUCCESS: {
            var wut = action.payload;

            return {
                ...state,
                loading: false,
                trendsloading: true,
                charts: [...state.charts, wut]
            };

        }
        default:
            return state;
    }
}
