import axios from 'axios';
import {
	getHomeSuccess, getHomeFailure, getHomeInitial,
	getObjectTreeFailure, getObjectTreeInitial, getObjectTreeSuccess,
	getPdfRulesFailure, getPdfRulesInitial, getPdfRulesSuccess, getSummaryFailure,
	getSummaryInitial, getSummarySuccess
} from './redux/actions';


export function getHomeData(){
	return (dispatch, getState) => { 
	
		dispatch(getHomeInitial());

		axios.get("/files.json")
			.then(
				(response) => {
					if (response['status'] === 200) {
						// Login the user using dispatch                
						dispatch(getHomeSuccess(response.data));
					} else { 
						// Send the error from API back
						dispatch(getHomeFailure(response));
					} 
				}
			);
			
	}
}

export function getPdfRuleDefinitions() {
	return (dispatch, getState) => {

		dispatch(getPdfRulesInitial());

		axios.get("/pdfrules.json")
			.then(
				(response) => {
					if (response['status'] === 200) {
						// Login the user using dispatch                
						dispatch(getPdfRulesSuccess(response.data));
					} else {
						// Send the error from API back
						dispatch(getPdfRulesFailure(response));
					}
				}
			);
	}
}

export function getSummary(file) {
	return (dispatch, getState) => {

		dispatch(getSummaryInitial());
		axios.all(
			[
				axios.get("/" + file + ".dat.json"),
				axios.get("/pdfrules.json")
			]
		).then(
			axios.spread(
				(summResponse, rulesResponse) => {
					if (summResponse['status'] === 200) {
						// Login the user using dispatch                
						dispatch(getSummarySuccess(summResponse.data));
					} else {
						// Send the error from API back
						dispatch(getSummaryFailure(summResponse));
					}

					if (rulesResponse['status'] === 200) {
						// Login the user using dispatch                
						dispatch(getPdfRulesSuccess(rulesResponse.data));
					} else {
						// Send the error from API back
						dispatch(getPdfRulesFailure(rulesResponse));
					}
				}


			)
		);
	
	}
}

export function getObjectTree(file) {
	return (dispatch, getState) => {

		dispatch(getObjectTreeInitial());

		axios.get("/" + file + ".obj.json")
			.then(
				(response) => {
					if (response['status'] === 200) {
						// Login the user using dispatch                
						dispatch(getObjectTreeSuccess(response.data));
					} else {
						// Send the error from API back
						dispatch(getObjectTreeFailure(response));
					}
				}
			);
	}
}


export function getDetailData() {
	return (dispatch, getState) => {

		dispatch(getHomeInitial());

		axios.get("/detail.json")
			.then(
				(response) => {
					if (response['status'] === 200) {
						// Login the user using dispatch                
						dispatch(getHomeSuccess(response.data));
					} else {
						// Send the error from API back
						dispatch(getHomeFailure(response));
					}
				}
			);
	}
}