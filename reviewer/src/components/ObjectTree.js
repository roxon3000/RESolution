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


    render() {
        var nodes = this.props.tree

        return (
            <Template>
                <div> Object Tree - add something here</div>
                <div>
                    
                </div>
                <Tree
                    contents={nodes}
                    //onNodeClick={handleNodeClick}
                    //onNodeCollapse={handleNodeCollapse}
                    //onNodeExpand={handleNodeExpand}
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