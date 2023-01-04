import * as React from "react";
import {
    GET_SUMMARY_FAILURE, GET_SUMMARY_SUCCESS, GET_SUMMARY_INITIAL
} from "../actionTypes";
import cloneDeep from "lodash/cloneDeep"; 


const INITIAL_STATE = {
    results :      
        {
            "id": "",
            "matchCount": 0,
        },
    loading: true

}
function listitize(data) {
    let newList = {
        id: data.id,
        matchCount: data.matchCount,
        matchedRules: []
        }
    for (let key in data) {
        switch (key) {
            case "id":
            case "matchCount":
                continue;
            default:
                for (let obj in data[key].objs) {
                    let item = {
                        id: data[key].id,
                        objectRefId: data[key].objs[obj].id,
                        ruleRefId: key
                    };
                    newList.matchedRules.push(item);
                }
        }
    }
    return newList;
    
}

export default function (state = INITIAL_STATE, action) {
    switch (action.type) {        
        case GET_SUMMARY_INITIAL:
            return { ...state };
        case GET_SUMMARY_SUCCESS:
            let serviceData = action.payload;            
            return {
                ...state,
                results: listitize(serviceData),
                loading: false
            };
        default:
            return state;
    }
}
