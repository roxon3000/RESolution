
import { combineReducers } from "redux";
import pdfreducer from "./pdfreducer";
import objecttree from "./objecttree";
import summary from "./summary";

//can add more reducers here
//const someReducer = combineReducers({ pdfreducer, someothereducer, etcreducer });
const someReducer = combineReducers({ pdfreducer, objecttree, summary }); 
export default someReducer;
