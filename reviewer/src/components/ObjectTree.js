import React, { useEffect } from 'react';
import { getObjectTree } from '../services';
import { connect, useDispatch, useSelector } from 'react-redux';
import Template from './Template'
import { Classes, Icon, Intent, Tree, TreeNodeInfo } from "@blueprintjs/core";
import { useSearchParams } from "react-router-dom";
import ObjectDialog from './ObjectDialog'

// example = https://github.com/palantir/blueprint/blob/develop/packages/docs-app/src/examples/core-examples/treeExample.tsx
//
function determineObjectType(obj) {

    if (obj && obj.objectNumber && obj.generationNumber) {
        return "PDF";
    }

    return "Unkown";
}

function ObjectTree(props) {

    const dispatch = useDispatch();
    let nodes = useSelector((state) => state.objecttree.tree);
    let selectedNode = useSelector((state) => state.objecttree.selectedNode);
    let selectedRawObj = useSelector((state) => state.objecttree.selectedRawObj);
    let openDialog = useSelector((state) => state.objecttree.openDialog);
    let objectType = determineObjectType(selectedRawObj);
    let selectedLabel = (selectedNode) ? selectedNode.label : null;
    let loading = useSelector(
        (state) => state.objecttree.loading
    );
    let [searchParams, setSearchParams] = useSearchParams();
    let file = searchParams.get('file');
    const entries = (selectedNode == null) ? [] : Object.entries(selectedNode).filter(entry => !Array.isArray(entry[1]));
    const listItems = (selectedNode == null) ? null : entries.map((attr) =>    
        <li key={attr[0]}>{attr[0]} : {String(attr[1])}
            </li>
    );   
    const rawEntries = (selectedRawObj == null) ? [] : Object.entries(selectedRawObj).filter(entry => !Array.isArray(entry[1]));
    const rawListItems = (selectedRawObj == null) ? null : rawEntries.map((attr) =>
        <li key={attr[0]}>{attr[0]} : {String(attr[1])}
        </li>
    );   

    useEffect(

        () => {
            if (loading) {
                dispatch(getObjectTree(file));
            }
        }

    );

    const handleDialogClose = () => {
        dispatch({
            payload: { dialogOpen: false },
            type: "CLOSE_DIALOG"
        });
    };

    const handleNodeDblClick = (node, nodePath, e) => {
        //const originallySelected = node.isSelected;
        //dispatch({
        //    payload: { path: nodePath, isSelected: originallySelected == null ? true : !originallySelected },
        //    type: "SET_IS_SELECTED"
        //});
        dispatch({
            payload: { path: nodePath, dialogOpen: true },
            type: "OPEN_IN_DIALOG"
        });
    };

    const handleNodeExpand = (node, nodePath) => {

        dispatch({
            payload: { path: nodePath, isExpanded: true },
            type: "SET_IS_EXPANDED"
        });
    }; 

    const handleNodeClick = (node, nodePath, e) => {
        const originallySelected = node.isSelected;

        if (!e.shiftKey) {
            dispatch({ type: "DESELECT_ALL" });
        }
        dispatch({
            payload: { path: nodePath, isSelected: originallySelected == null ? true : !originallySelected },
            type: "SET_IS_SELECTED"
        })
    };

    const handleNodeCollapse = (_node, nodePath) => {
        dispatch({
            payload: { path: nodePath, isExpanded: false },
            type: "SET_IS_EXPANDED"
        });
    };
    return (
        
        <div className="container">
            <div className="row">
                <div className="col-lg">
                    <h3>Object Tree</h3>
                </div>
            </div>
            <div className="row">
                <div className="col-lg">
                    <Tree
                        contents={nodes}
                        onNodeClick={handleNodeClick}
                        onNodeCollapse={handleNodeCollapse}
                        onNodeExpand={handleNodeExpand}
                        onNodeDoubleClick={handleNodeDblClick }
                        className={Classes.ELEVATION_0}
                    />
                </div>
                {selectedNode && 
                    <div className="col-lg">
                        <div className="container">
                            <div className="col-sm">
                                <b>Selected Node</b>
                                <ul>
                                    {listItems}
                                </ul>
                                <b>Selected Raw Object</b>
                                <ul>
                                    {rawListItems}
                                </ul>

                            </div>
                        </div>
                    </div>
                }
            </div>
            <ObjectDialog
                isOpen={openDialog}
                onClose={handleDialogClose}
                selectedObject={selectedRawObj}
                objectType={objectType}
                label={selectedLabel}
            />
        </div>


    

    );
}

export default ObjectTree;