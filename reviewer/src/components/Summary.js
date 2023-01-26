import React, { useEffect } from 'react';
import { getSummary } from '../services';
import { useDispatch, useSelector } from 'react-redux';
import { useSearchParams } from "react-router-dom";
import RuleDisplay from './RuleDisplay';
import ObjectDialog from './ObjectDialog';
import { determineObjectType } from './ObjectTree';
import { Button } from "@blueprintjs/core";

// example = https://github.com/palantir/blueprint/blob/develop/packages/docs-app/src/examples/core-examples/treeExample.tsx
//

function Summary(props) {

    const dispatch = useDispatch();
    let matchedRules = useSelector((state) => state.summary.results.matchedRules);
    let rules = useSelector((state) => state.summary.rules);

    let objs = props.objs;
    let selectedRawObj = useSelector((state) => state.objecttree.selectedRawObj);
    let openDialog = useSelector((state) => state.objecttree.openDialog);
    let objectType = determineObjectType(selectedRawObj);
    let selectedLabel = (selectedRawObj) ? "OBJ " + selectedRawObj.objectNumber : null;

    let loading = useSelector(
        (state) => state.summary.loading
    );
    let [searchParams, setSearchParams] = useSearchParams();
    let file = searchParams.get('file');

    let htmlRows = (matchedRules == null) ? null : matchedRules.map((attr) =>
        <tr key="{attr.id}">
            <td><Button onClick={(e) => handleClick(e)} value={attr.objectRefId} >OBJ {attr.objectRefId}</Button> </td>
            <td><RuleDisplay rules={rules} ruleId={attr.ruleRefId} /></td>
        </tr>
    );

    const handleDialogClose = () => {
        dispatch({
            payload: { dialogOpen: false },
            type: "CLOSE_DIALOG"
        });
    };

    const handleClick = (e) => {
        dispatch({
            payload: { selecteRawObjId: e.currentTarget.value, dialogOpen: true },
            type: "OPEN_IN_DIALOG_T"
        });
    };
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
                            {htmlRows}
                        </tbody>
                    
                    </table>
                </div>
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

export default Summary;