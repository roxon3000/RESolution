import * as React from "react";
import {
    GET_OBJ_TREE_INITIAL, GET_OBJ_TREE_SUCCESS
} from "../actionTypes";
import { Classes, Icon, Intent, Tree, TreeNodeInfo } from "@blueprintjs/core";
import { ContextMenu2, Classes as Popover2Classes, Tooltip2 } from "@blueprintjs/popover2";
import cloneDeep from "lodash/cloneDeep"; 
import { Example, ExampleProps } from "@blueprintjs/docs-theme";


const contentSizing = { popoverProps: { popoverClassName: Popover2Classes.POPOVER2_CONTENT_SIZING } };
const INITIAL_STATE = {
    tree : 
        [
            {
                id: 0,
                hasCaret: false,
                icon: "folder-close",
                label: ""
            }
        ],
    loading: true,
    raw: null,
    selectedNode: null,
    openDialog: false

}

/*
type NodePath = number[];

type TreeAction =
    | { type: "SET_IS_EXPANDED"; payload: { path: NodePath; isExpanded: boolean } }
    | { type: "DESELECT_ALL" }
    | { type: "SET_IS_SELECTED"; payload: { path: NodePath; isSelected: boolean } };
    */
function forEachNode(nodes, callback) {
    if (nodes === undefined) {
        return;
    }

    for (const node of nodes) {
        callback(node);
        forEachNode(node.childNodes, callback);
    }
}

function forNodeAtPath(nodes, path, callback) {
    callback(Tree.nodeFromPath(path, nodes));
}

function findRawObj(refId, raw) {
    return (refId === "trailer") ? raw.treeTrailer : raw.objectMap[refId];
}

function generateObjectBranch(node, rawObj) {
    if (rawObj == null) {
        return;
    }

    let trailer = {
        id: rawObj.id,
        hasCaret: true,
        icon: "circle",
        label: rawObj.objectNumber,
        isExpanded: false,
        childNodes: null
    }
    //special edit for trailer
    if (rawObj.objectNumber === "trailer") {
        node = trailer;
        node.ref = rawObj.objectNumber;
    }
    let propCount = 0;
    for (var key in rawObj) {
        if (node.childNodes == null) {
            node.childNodes = [];
        }
        propCount = propCount + 1;
        let propObj = rawObj[key];
        let propNode = null;
        //if rawObj is a JSON Ref, then add ref to node for lazy loading in UI component
        if (propObj != null && typeof propObj === "object" && propObj.hasOwnProperty("$ref")) {
            let label = key + " #" + propObj.id;
            propNode = newNode(rawObj.id + key, true, 'circle', label, false);
            propNode.ref = propObj["id"];
            propNode.isArray = false;
            propNode.isObject = true;
            node.childNodes.push(propNode);
        } else if (Array.isArray(propObj)) {
            propNode = newNode(rawObj.id + key + String(propCount), true, 'array', key, false);
            propNode.isArray = true;
            propNode.isObject = false;
            //propNode.ref = rawObj.objectNumber + "," + key;
            propNode.ref = node.ref + ',' + key
            node.childNodes.push(propNode);
        } else if (typeof propObj === "object") {
            let label = key;
            propNode = newNode(rawObj.id + key, true, 'circle', label, false);
            propNode.isArray = false;
            propNode.isObject = true;
            propNode.ref = node.ref + ',' + key
            node.childNodes.push(propNode);
            generateObjectBranch(propNode, propObj)
        } 
        
    }
    //check for empty child nodes. this is necessary because of lazy loading
    if (node.childNodes.length === 0) {
        node.hasCaret = false;
    }
    return node
}

function dereference(rawRef, raw) {
    let ref = rawRef.split(",");
    let rawParentObj = findRawObj(ref[0], raw);
    let rawObj = rawParentObj; // rawParentObj[ref[1]];
    let tempParent = rawParentObj;
    for (let ri = 1; ri < ref.length; ri++) {
        let interObject = tempParent[ref[ri]];

        if (ri < (ref.length - 1)) {
            tempParent = interObject;
        } else {
            rawObj = interObject;
        }
    }

    return rawObj;
}

function generateList(expNode, raw) { 
    if (expNode == null || expNode.ref == null) {
        return;
    }

    let rawObj = dereference(expNode.ref, raw);

    expNode.childNodes = [];
    let propCount = 0;
    for (var key in rawObj) {
     
        propCount = propCount + 1;
        let propObj = rawObj[key];
        
        let propNode = null
        //if rawObj is a JSON Ref, then add ref to node for lazy loading in UI component
        if (typeof propObj === "object" && propObj.hasOwnProperty("$ref")) {
            let label = "OBJ #" + propObj.id
            propNode = newNode(propObj.id + key, true, 'circle', label, false)
            propNode.ref = propObj.id;
            propNode.isArray = false
            propNode.isObject = true
            expNode.childNodes.push(propNode)
        } else if (Array.isArray(propObj)) {
            //to limit potentil recursive loops, may need to remove support of lists within lists. 
            propNode = newNode(propObj.id + key + String(propCount), true, 'array', key, false)
            propNode.isArray = true
            propNode.isObject = false
            propNode.ref = propObj.objectNumber + "," + key;
            expNode.childNodes.push(propNode)
        } else {
            let primNode = newNode(expNode.ref + String(propCount), false, "citation", rawObj[key], false);
            primNode.isArray = false;
            primNode.isObject = false;
            expNode.childNodes.push(primNode);
            
        }

    }

}

function newNode(id, hasCaret, icon, label, isExpanded) {
    var node = {
        id: id,
        hasCaret: hasCaret,
        icon: icon,
        label: label,
        isExpanded: isExpanded
    }
    return node
}

export default function (state = INITIAL_STATE, action) {
    switch (action.type) {
        case "OPEN_IN_DIALOG_T":
            const newState6 = cloneDeep(state);
            newState6.openDialog = true;
            newState6.selectedRawObj = findRawObj(action.payload.selecteRawObjId, newState6.raw);
            return newState6;
        case "CLOSE_DIALOG":
            const newState5 = cloneDeep(state);
            newState5.openDialog = false;
            return newState5;
        case "OPEN_IN_DIALOG":
            const newState4 = cloneDeep(state);
            newState4.openDialog = true;
            return newState4;
        case "DESELECT_ALL":
            const newState1 = cloneDeep(state);
            forEachNode(newState1.tree, node => (node.isSelected = false));
            return newState1;
        case "SET_IS_EXPANDED":
            const newState2 = cloneDeep(state);
            forNodeAtPath(
                newState2.tree,
                action.payload.path,
                node => {
                    node.isExpanded = action.payload.isExpanded
                    newState2.expandedNode = node
                });
            if (action.payload.isExpanded === true &&
                newState2.expandedNode.childNodes === undefined &&
                newState2.expandedNode.isObject === true) {
                let exprawObj = findRawObj(newState2.expandedNode.ref, newState2.raw);
                generateObjectBranch(newState2.expandedNode, exprawObj)
            } else if (action.payload.isExpanded === true &&
                newState2.expandedNode.childNodes === undefined &&
                newState2.expandedNode.isArray === true) {

                generateList(newState2.expandedNode, newState2.raw) 
            }
            return newState2;
        case "SET_IS_SELECTED":
            const newState3 = cloneDeep(state);
            forNodeAtPath(
                newState3.tree,
                action.payload.path,
                node => {
                    node.isSelected = action.payload.isSelected;
                    newState3.selectedNode = node
                }
            );
            newState3.selectedRawObj = dereference(newState3.selectedNode.ref, newState3.raw);
            return newState3;
        case GET_OBJ_TREE_INITIAL:
            return {
                ...state,
                loading: true
            };
        case GET_OBJ_TREE_SUCCESS:
            let serviceData = action.payload;            
            let tree = [];
            tree.push(generateObjectBranch(null, serviceData.treeTrailer))
            return {
                ...state,
                tree: tree,
                raw: serviceData,
                loading: false
            };
        default:
            return state;
    }
}
