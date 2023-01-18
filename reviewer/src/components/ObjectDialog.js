import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Button, Dialog, DialogBody, DialogFooter } from "@blueprintjs/core"

// example = https://github.com/palantir/blueprint/blob/develop/packages/docs-app/src/examples/core-examples/treeExample.tsx
//

function ObjectDialog(props) {

    const dispatch = useDispatch();
    let matchedRules = useSelector((state) => state.summary.results.matchedRules);
    let openDialog = props.isOpen;
    let handleClose = props.onClose;

    //let selectedNode = useSelector((state) => state.objecttree.selectedNode);
    //let selectedRawObj = useSelector((state) => state.objecttree.selectedRawObj);

    let loading = useSelector(
        (state) => state.summary.loading
    );

    const footerActions = (
        <>
            <Button onClick={handleClose}>Close</Button>
        </>
    );

    //const rawEntries = (selectedRawObj == null) ? [] : Object.entries(selectedRawObj).filter(entry => !Array.isArray(entry[1]));
    //const rawListItems = (selectedRawObj == null) ? null : rawEntries.map((attr) =>
    //    <li key={attr[0]}>{attr[0]} : {String(attr[1])}
    //    </li>
    //);

    useEffect(

        () => {
            if (loading) {
                //dispatch(getSummary(file));
            }
        }

    );

    return (

        <div className="container">
            <div className="row">
                <div className="col-lg">
                    <Dialog title="Put Object ID info here" isOpen={openDialog} onClose={handleClose} icon="info-sign">
                        <DialogBody>
                            Dynamic Object Data goes here
                        </DialogBody>                        
                        <DialogFooter actions={footerActions}></DialogFooter>
                    </Dialog>
                </div>
            </div>
        </div>




    );
}

export default ObjectDialog;