import React from 'react';
import { getDetailData } from '../services';
import { connect } from 'react-redux';
import Template from './Template'
import { TreeExample } from '../redux/reducers/exampletree'

// example = https://github.com/palantir/blueprint/blob/develop/packages/docs-app/src/examples/core-examples/treeExample.tsx
// 

class ExampleTree extends React.Component {

    constructor(props) {
        super(props)

    }


    render() {
        var tree = this.props.tree

        return (
            <Template>
                <TreeExample></TreeExample>
            </Template>

        );
    }
}


const mapDispatchToProps = dispatch => {
    return {
        loadTrendData: () => {
            dispatch(getDetailData());
        }
    }
}

const mapStateToProps = state =>
(
    {
        tree: state,
        loading: state
    }
)

export default connect(mapStateToProps, mapDispatchToProps)(ExampleTree);