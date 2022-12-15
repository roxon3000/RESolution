import {
    GET_TRENDS_INITIAL, GET_TRENDS_SUCCESS,
    GET_PTRENDS_INITIAL, GET_PTRENDS_SUCCESS,
    GET_HOME_INITIAL, GET_HOME_SUCCESS, GET_DPHRASE_SUCCESS
} from "../actionTypes";

const initialState = {
    pdfreducer: {
        files: {}
    },
    loading: false,
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
                files: serviceData.files,
                loading: false
            };
        }
        default:
            return { ...state
                 }
;
    }
}
