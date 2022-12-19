import React, { useEffect } from 'react';
import { getObjectTree } from '../services';
import { connect, useDispatch, useSelector } from 'react-redux';
import Template from './Template'
import { Classes, Icon, Intent, Tree, TreeNodeInfo } from "@blueprintjs/core";
import { useParams } from "react-router-dom"

// example = https://github.com/palantir/blueprint/blob/develop/packages/docs-app/src/examples/core-examples/treeExample.tsx
//

function ObjectTree(props) {

    const dispatch = useDispatch();
    var nodes = useSelector((state) => state.objecttree.tree);
    var loading = useSelector(
        (state) => state.objecttree.loading
    );

    useEffect(

        () => {
            if (loading) {
                dispatch(getObjectTree());
            }
        }

    );

    const handleNodeExpand = (node, nodePath) => {

        dispatch({
            payload: { path: nodePath, isExpanded: true },
            type: "SET_IS_EXPANDED",
        });
    }; 

    const handleNodeClick = (node, nodePath, e) => {
        const originallySelected = node.isSelected;

        if (!e.shiftKey) {
            dispatch({ type: "DESELECT_ALL" });
        }
        dispatch({
            payload: { path: nodePath, isSelected: originallySelected == null ? true : !originallySelected },
            type: "SET_IS_SELECTED",
        })
    };

    const handleNodeCollapse = (_node, nodePath) => {
        dispatch({
            payload: { path: nodePath, isExpanded: false },
            type: "SET_IS_EXPANDED",
        });
    };
    return (
        <Template>
            <div> Object Tree - add something here</div>
            <div>

            </div>
            <Tree
                contents={nodes}
                onNodeClick={handleNodeClick}
                onNodeCollapse={handleNodeCollapse}
                onNodeExpand={handleNodeExpand}
                className={Classes.ELEVATION_0}
            />


        </Template>

    );
}

export default ObjectTree;