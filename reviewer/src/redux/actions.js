import {
    SET_FILTER, GET_OBJ_TREE_INITIAL, GET_OBJ_TREE_SUCCESS, GET_OBJ_TREE_FAILURE,
  GET_HOME_INITIAL, GET_HOME_SUCCESS, GET_HOME_FAILURE  } from "./actionTypes";

 
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
