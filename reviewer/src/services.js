import axios from 'axios';
import {
	getHomeSuccess, getHomeFailure, getHomeInitial,
	getObjectTreeFailure, getObjectTreeInitial, getObjectTreeSuccess
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

export function getObjectTree(file) {
	return (dispatch, getState) => {

		dispatch(getObjectTreeInitial());

		axios.get("/" + file)
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