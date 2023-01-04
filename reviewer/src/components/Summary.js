import React, { useEffect } from 'react';
import { getSummary } from '../services';
import { useDispatch, useSelector } from 'react-redux';
import { useSearchParams } from "react-router-dom";


// example = https://github.com/palantir/blueprint/blob/develop/packages/docs-app/src/examples/core-examples/treeExample.tsx
//

function Summary(props) {

    const dispatch = useDispatch();
    let matchedRules = useSelector((state) => state.summary.results.matchedRules);
    //let selectedNode = useSelector((state) => state.objecttree.selectedNode);
    //let selectedRawObj = useSelector((state) => state.objecttree.selectedRawObj);

    let loading = useSelector(
        (state) => state.summary.loading
    );
    let [searchParams, setSearchParams] = useSearchParams();
    let file = searchParams.get('file');

    //const entries = (selectedNode == null) ? [] : Object.entries(selectedNode).filter(entry => !Array.isArray(entry[1]));
    const rows = (matchedRules == null) ? null : matchedRules.map((attr) =>
        <div key="{attr.id}" className="row">
            <div className="col-sm">{attr.id}</div>
            <div className="col-sm">{attr.objectRefId}</div>
            <div className="col-sm">{attr.ruleRefId}</div>
        </div>
    );
    const htmlRows = (matchedRules == null) ? null : matchedRules.map((attr) =>
        <tr key="{attr.id}" className="row">
            <td className="col-sm">{attr.id}</td>
            <td className="col-sm">{attr.objectRefId}</td>
            <td className="col-sm">{attr.ruleRefId}</td>
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
                    Summary Rules Results here
                        <div key="header" className="row">
                            <div className="col-sm">ID</div>
                            <div className="col-sm">Object Ref ID</div>
                            <div className="col-sm">Rule Ref ID</div>
                        </div>
                        <div className="container">
                            {rows}
                        </div>

                        <table>
                            <tr>
                                <td>
                                    Col1
                                </td>
                                <td>
                                    Col2
                                </td>
                                <td>
                                    Col3
                                </td>
                            </tr>
                        {htmlRows}
                        </table>
                    </div>
                </div>
            </div>




    );
}

export default Summary;