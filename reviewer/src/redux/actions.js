import {
    SET_FILTER, GET_OBJ_TREE_INITIAL, GET_OBJ_TREE_SUCCESS, GET_OBJ_TREE_FAILURE,
    GET_HOME_INITIAL, GET_HOME_SUCCESS, GET_HOME_FAILURE, GET_PDF_RULES_FAILURE,
    GET_PDF_RULES_INITIAL, GET_PDF_RULES_SUCCESS, GET_SUMMARY_FAILURE, GET_SUMMARY_INITIAL,
    GET_SUMMARY_SUCCESS
} from "./actionTypes";

export const getSummaryInitial = parm1 => ({
    type: GET_SUMMARY_INITIAL
});

export const getSummarySuccess = data => ({
    type: GET_SUMMARY_SUCCESS,
    payload: data
});

export const getSummaryFailure = data => ({
    type: GET_SUMMARY_FAILURE,
    payload: data
});

export const getPdfRulesInitial = parm1 => ({
    type: GET_PDF_RULES_INITIAL
});

export const getPdfRulesSuccess = data => ({
    type: GET_PDF_RULES_SUCCESS,
    payload: data
});

export const getPdfRulesFailure = data => ({
    type: GET_PDF_RULES_FAILURE,
    payload: data
});

export const getObjectTreeInitial = parm1 => ({
    type: GET_OBJ_TREE_INITIAL
});

export const getObjectTreeSuccess = data => ({
    type: GET_OBJ_TREE_SUCCESS,
  payload: data
});

export const getObjectTreeFailure = data => ({
    type: GET_OBJ_TREE_FAILURE,
  payload: data
});

export const getHomeInitial = parm1 => ({
  type: GET_HOME_INITIAL
});

export const getHomeSuccess = data => ({
  type: GET_HOME_SUCCESS,
  payload: data
});

export const getHomeFailure = data => ({
  type: GET_HOME_FAILURE,
  payload: data
});

export const setFilter = filter => ({ type: SET_FILTER, payload: { filter } });
