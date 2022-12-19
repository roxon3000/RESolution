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
    raw : null

    }
const INITIAL_STATE_example =
[
    {
        id: 0,
        hasCaret: true,
        icon: "folder-close",
        label: (
            <ContextMenu2 {...contentSizing} content={<div>Hello there!</div>}>
                Folder 0
            </ContextMenu2>
        ),
    },
    {
        id: 1,
        icon: "folder-close",
        isExpanded: true,
        label: (
            <ContextMenu2 {...contentSizing} content={<div>Hello there!</div>}>
                <Tooltip2 content="I'm a folder <3" placement="right">
                    Folder 1
                </Tooltip2>
            </ContextMenu2>
        ),
        childNodes: [
            {
                id: 2,
                icon: "document",
                label: "Item 0",
                secondaryLabel: (
                    <Tooltip2 content="An eye!">
                        <Icon icon="eye-open" />
                    </Tooltip2>
                ),
            },
            {
                id: 3,
                icon: <Icon icon="tag" intent={Intent.PRIMARY} className={Classes.TREE_NODE_ICON} />,
                label: "Organic meditation gluten-free, sriracha VHS drinking vinegar beard man.",
            },
            {
                id: 4,
                hasCaret: true,
                icon: "folder-close",
                label: (
                    <ContextMenu2 {...contentSizing} content={<div>Hello there!</div>}>
                        <Tooltip2 content="foo" placement="right">
                            Folder 2
                        </Tooltip2>
                    </ContextMenu2>
                ),
                childNodes: [
                    { id: 5, label: "No-Icon Item" },
                    { id: 6, icon: "tag", label: "Item 1" },
                    {
                        id: 7,
                        hasCaret: true,
                        icon: "folder-close",
                        label: (
                            <ContextMenu2 {...contentSizing} content={<div>Hello there!</div>}>
                                Folder 3
                            </ContextMenu2>
                        ),
                        childNodes: [
                            { id: 8, icon: "document", label: "Item 0" },
                            { id: 9, icon: "tag", label: "Item 1" },
                        ],
                    },
                ],
            },
        ],
    },
    {
        id: 2,
        hasCaret: true,
        icon: "folder-close",
        label: "Super secret files",
        disabled: true,
    },
    ];
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

function generateObjectTree(rawData, layers) {
    /* 
     {
        id: 0,
        hasCaret: true,
        icon: "folder-close",
        label: (
            <ContextMenu2 {...contentSizing} content={<div>Hello there!</div>}>
                Folder 0
            </ContextMenu2>
        ),
    },
   */
    var objectTree = []
    var trailer = {
        id: rawData.treeTrailer.id,
        hasCaret: true,
        icon: "flow-branch",
        label: rawData.treeTrailer.objectNumber,
        isExpanded: true,
        childNodes: []
    }
    for (var key in rawData.treeTrailer){
        var node = newNode(trailer.id + key, false, 'flow-end', key, false)
        trailer.childNodes.push(node)
    }


    objectTree.push(trailer)

    return objectTree
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
        case "DESELECT_ALL":
            const newState1 = cloneDeep(state);
            forEachNode(newState1.tree, node => (node.isSelected = false));
            return newState1;
        case "SET_IS_EXPANDED":
            const newState2 = cloneDeep(state);
            forNodeAtPath(newState2.tree, action.payload.path, node => (node.isExpanded = action.payload.isExpanded));
            return newState2;
        case "SET_IS_SELECTED":
            const newState3 = cloneDeep(state);
            forNodeAtPath(newState3.tree, action.payload.path, node => (node.isSelected = action.payload.isSelected));
            return newState3;
        case GET_OBJ_TREE_INITIAL:
            return state;
        case GET_OBJ_TREE_SUCCESS:
            var serviceData = action.payload;
            var  tree = generateObjectTree(serviceData, 3)
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
