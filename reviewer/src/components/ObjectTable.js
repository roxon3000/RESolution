import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import ObjectDialog from './ObjectDialog';
import { determineObjectType } from './ObjectTree';
import { Button } from "@blueprintjs/core";

function ObjectTable(props) {

    const dispatch = useDispatch();
    let objs = props.objs;
    let selectedRawObj = useSelector((state) => state.objecttree.selectedRawObj);
    let openDialog = useSelector((state) => state.objecttree.openDialog);
    let objectType = determineObjectType(selectedRawObj);
    let selectedLabel = (selectedRawObj) ? "OBJ " + selectedRawObj.objectNumber : null;


    let loading = useSelector(
        (state) => state.summary.loading
    );

    const handleDialogClose = () => {
        dispatch({
            payload: { dialogOpen: false },
            type: "CLOSE_DIALOG"
        });
    };

    const handleClick = (e) => {
        //const originallySelected = node.isSelected;
        //dispatch({
        //    payload: { path: nodePath, isSelected: originallySelected == null ? true : !originallySelected },
        //    type: "SET_IS_SELECTED"
        //});
        dispatch({
            payload: { selecteRawObjId: e.currentTarget.value, dialogOpen: true },
            type: "OPEN_IN_DIALOG_T"
        });
    };

    const objRows = (objs == null) ? [] : Object.entries(objs).map(obj =>
        <tr key={obj[1].id}>
            <td><Button onClick={(e) => handleClick(e)} value={obj[0]} >OBJ {obj[0]}</Button> </td>
        </tr>
    );
    useEffect(

        () => {
            if (loading) {
                //dispatch(getSummary(file));
            }
        }

    );

    return (
        <>
            <div className="container">
                <div className="row">
                    <div className="col-lg">
                        <h3>Object Table</h3>
                    </div>
                </div>
                <div className="row">
                    <div className="col-lg">
                        <table>
                            <tbody>
                                <tr>
                                    <td><strong>ID</strong></td>
                                </tr>
                                {true && objRows }
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <ObjectDialog
                isOpen={openDialog}
                onClose={handleDialogClose}
                selectedObject={selectedRawObj}
                objectType={objectType}
                label={selectedLabel}
            />
        </>
    );
}

export default ObjectTable;