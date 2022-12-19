import React from 'react';
import { getObjectTree } from '../services';
import { connect } from 'react-redux';
import Template from './Template'
import { Classes, Icon, Intent, Tree, TreeNodeInfo } from "@blueprintjs/core";

// example = https://github.com/palantir/blueprint/blob/develop/packages/docs-app/src/examples/core-examples/treeExample.tsx
// 

class ObjectTree extends React.Component {

    constructor(props) {
        super(props)
        this.props.loadObjTreeData()
    }
    /*
    handleNodeClick = React.useCallback(
        (node, nodePath, e) => {
            const originallySelected = node.isSelected;
            if (!e.shiftKey) {
                dispatch({ type: "DESELECT_ALL" });
            }
            dispatch({
                payload: { path: nodePath, isSelected: originallySelected == null ? true : !originallySelected },
                type: "SET_IS_SELECTED",
            });
        },
        [],
    );

    handleNodeCollapse = React.useCallback((_node, nodePath) => {
        dispatch({
            payload: { path: nodePath, isExpanded: false },
            type: "SET_IS_EXPANDED",
        });
    }, []);

    handleNodeExpand = React.useCallback((_node, nodePath) => {
        dispatch({
            payload: { path: nodePath, isExpanded: true },
            type: "SET_IS_EXPANDED",
        });
    }, []);
    */

    render() {
        var nodes = this.props.tree

        return (
            <Template>
                <div> Object Tree - add something here</div>
                <div>
                    
                </div>
                <Tree
                    contents={nodes}
                    onNodeClick={this.props.handleNodeClick}
                    onNodeCollapse={this.props.handleNodeCollapse}
                    onNodeExpand={this.props.handleNodeExpand}
                    className={Classes.ELEVATION_0}
                />

                
            </Template>

        );
    }
}


const mapDispatchToProps = dispatch => {
    return {
        loadObjTreeData: () => {
            dispatch(getObjectTree());
        },
        handleNodeExpand: (node, nodePath) => {
            dispatch({
                payload: { path: nodePath, isExpanded: true },
                type: "SET_IS_EXPANDED",
            });
        },
        handleNodeClick: (node, nodePath, e) => {
            const originallySelected = node.isSelected;
            if (!e.shiftKey) {
                dispatch({ type: "DESELECT_ALL" });
            }
            dispatch({
                payload: { path: nodePath, isSelected: originallySelected == null ? true : !originallySelected },
                type: "SET_IS_SELECTED",
            });
        },
        handleNodeCollapse: (_node, nodePath) => {
            dispatch({
                payload: { path: nodePath, isExpanded: false },
                type: "SET_IS_EXPANDED",
            });
        }
    }
}

const mapStateToProps = state =>
(
    {
        tree: state.objecttree.tree,
        loading: state
    }
)


export default connect(mapStateToProps, mapDispatchToProps)(ObjectTree);