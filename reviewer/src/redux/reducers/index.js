
import { combineReducers } from "redux";
import pdfreducer from "./pdfreducer";
import objecttree from "./objecttree"

//can add more reducers here
//const someReducer = combineReducers({ pdfreducer, someothereducer, etcreducer });
const someReducer = combineReducers({ pdfreducer, objecttree }); 
export default someReducer;
