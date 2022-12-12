import { SET_FILTER, GET_TRENDS_INITIAL, GET_TRENDS_SUCCESS, GET_TRENDS_FAILURE,
  GET_PTRENDS_INITIAL, GET_PTRENDS_SUCCESS, GET_PTRENDS_FAILURE,
  GET_HOME_INITIAL, GET_HOME_SUCCESS, GET_HOME_FAILURE,
  GET_DPHRASE_FAILURE, GET_DPHRASE_INITIAL, GET_DPHRASE_SUCCESS} from "./actionTypes";

  export const getDailyPhrasesInitial = parm1 => ({
    type: GET_DPHRASE_INITIAL
  });
  
  export const getDailyPhrasesSuccess = data => ({
    type: GET_DPHRASE_SUCCESS,
    payload: data
  });
  
  export const getDailyPhrasesFailure = data => ({
    type: GET_DPHRASE_FAILURE,
    payload: data
  });

export const getPersistentTrendsInitial = parm1 => ({
  type: GET_PTRENDS_INITIAL
});

export const getPersistentTrendsSuccess = data => ({
  type: GET_PTRENDS_SUCCESS,
  payload: data
});

export const getPersistentTrendsFailure = data => ({
  type: GET_PTRENDS_FAILURE,
  payload: data
});

export const getTrendsInitial = parm1 => ({
  type: GET_TRENDS_INITIAL
});

export const getTrendsSuccess = data => ({
  type: GET_TRENDS_SUCCESS,
  payload: data
});

export const getTrendsFailure = data => ({
  type: GET_TRENDS_FAILURE,
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
