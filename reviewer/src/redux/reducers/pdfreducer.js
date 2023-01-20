import {
    GET_HOME_INITIAL, GET_HOME_SUCCESS, GET_PDF_RULES_SUCCESS
} from "../actionTypes";

const initialState = {
    files: [],
    loading: false
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
