import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Button, Drawer, DrawerSize } from "@blueprintjs/core"

function ObjectDialog(props) {

    const dispatch = useDispatch();
    //let matchedRules = useSelector((state) => state.summary.results.matchedRules);
    let openDialog = props.isOpen;
    let handleClose = props.onClose;
    let objectType = props.objectType;
    let selectedObject = props.selectedObject;
    let label = props.label;
    const title = (label) ? label : "No Label";

    const rawEntries = (selectedObject == null) ? [] : Object.entries(selectedObject).filter(entry => !Array.isArray(entry[1]));
    const rawListItems = (selectedObject == null) ? null : rawEntries.map((attr) =>
        (attr[0] == "raw" || attr[0] == "stream" || attr[0] == "unfilteredStream") ? "" :
        <tr>
            <td>{attr[0]}</td>
            <td>{String(attr[1])}</td>
        </tr>
    );  
    //const title = (objectType) ? objectType : "Test";
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


    useEffect(

        () => {
            if (loading) {
                //dispatch(getSummary(file));
            }
        }

    );

    return (

        <Drawer title={title} isOpen={openDialog} onClose={handleClose} icon="folder-open" size={DrawerSize.LARGE }>
            <div className="container, object-drawer">
                <div className="row">
                    <div className="col">
                        <table>
                            <tbody>
                                {
                                    true && rawListItems
                                }
                            </tbody>
                        </table>
                    </div>
                </div>
                <div className="row">
                    <div className="col">
                        Raw Meta Data: <pre class="bp4-code-block"><code> {selectedObject && selectedObject.raw} </code></pre>
                    </div>
                </div>
                <div className="row">
                    <div className="col">
                        Raw Data Stream (Base64): <pre class="bp4-code-block"><code> {selectedObject && selectedObject.stream} </code></pre>
                    </div>
                </div>
            </div>
            {
                true && footerActions
            }
        </Drawer>
    );
}

export default ObjectDialog;