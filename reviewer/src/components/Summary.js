import React, { useEffect } from 'react';
import { getSummary } from '../services';
import { useDispatch, useSelector } from 'react-redux';
import { useSearchParams } from "react-router-dom";
import RuleDisplay from './RuleDisplay';

// example = https://github.com/palantir/blueprint/blob/develop/packages/docs-app/src/examples/core-examples/treeExample.tsx
//

function Summary(props) {

    const dispatch = useDispatch();
    let matchedRules = useSelector((state) => state.summary.results.matchedRules);
    let rules = useSelector((state) => state.summary.rules);
    //let selectedNode = useSelector((state) => state.objecttree.selectedNode);
    //let selectedRawObj = useSelector((state) => state.objecttree.selectedRawObj);

    let loading = useSelector(
        (state) => state.summary.loading
    );
    let [searchParams, setSearchParams] = useSearchParams();
    let file = searchParams.get('file');

    let htmlRows = (matchedRules == null) ? null : matchedRules.map((attr) =>
        <tr key="{attr.id}">
            <td>{attr.objectRefId}</td>
            <td><RuleDisplay rules={rules} ruleId={attr.ruleRefId} /></td>
        </tr>
    );

    //const rawEntries = (selectedRawObj == null) ? [] : Object.entries(selectedRawObj).filter(entry => !Array.isArray(entry[1]));
    //const rawListItems = (selectedRawObj == null) ? null : rawEntries.map((attr) =>
    //    <li key={attr[0]}>{attr[0]} : {String(attr[1])}
    //    </li>
    //);

    useEffect(

        () => {
            if (loading) {
                dispatch(getSummary(file));
            }
        }

    );

    return (

        <div className="container">
            <div className="row">
                <div className="col-lg">
                    <h3>Rules Summary</h3>
                </div>
            </div>
            <div className="row">
                <div className="col-lg">
                    <table className="app-table">
                        <tbody>
                            <tr>
                                <td>
                                    Object ID
                                </td>
                                <td>
                                    Rule ID
                                </td>
                            </tr>
                        </tbody>
                    {htmlRows}
                    </table>
                </div>
            </div>
            </div>




    );
}

export default Summary;