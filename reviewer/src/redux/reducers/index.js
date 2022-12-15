
import { combineReducers } from "redux";
import pdfreducer from "./pdfreducer";


//can add more reducers here
//const someReducer = combineReducers({ pdfreducer, someothereducer, etcreducer });
const someReducer = combineReducers({ pdfreducer }); 
export default someReducer;
