import React, { useEffect } from 'react';
import Template from './Template';
import Summary from './Summary';
import ObjectTree from './ObjectTree';
import ObjectTable from './ObjectTable';
import { useSearchParams } from "react-router-dom";
import { getObjectTree } from '../services';
import { useDispatch, useSelector } from 'react-redux';
import { Tab, Tabs } from "@blueprintjs/core";

function Detail(props) {
    const dispatch = useDispatch();
    let [searchParams, setSearchParams] = useSearchParams();
    let nodes = useSelector((state) => state.objecttree.tree);
    let selectedNode = useSelector((state) => state.objecttree.selectedNode);
    let selectedRawObj = useSelector((state) => state.objecttree.selectedRawObj);
    let openDialog = useSelector((state) => state.objecttree.openDialog);
    let selectedTab = useSelector((state) => state.objecttree.selectedTab);

    let file = searchParams.get('file');
    let loading = useSelector(
        (state) => state.objecttree.loading
    );
    let objs = useSelector((state) => (state.objecttree.raw) ? state.objecttree.raw.objectMap : null);

    useEffect(

        () => {
            if (loading) {
                dispatch(getObjectTree(file));
            }
        }

    );

    const handleNavbarTabChange = (navbarTabId) => {
        dispatch({
            payload: { selectedTab: navbarTabId },
            type: "CHANGE_TAB"
        });
    };
    
    return (
        <Template>
            <div className="container">
                <div className="row">
                    <div className="col">
                        <h1>Selected File: {file}</h1>
                    </div>
                </div>
                <div className="row">
                    <div className="col">

                        <Tabs id="viewertabs" onChange={handleNavbarTabChange} selectedTab={selectedTab} large={true} >
                            <Tab id="sm" title="Summary" panel={
                                <Summary
                                objs={objs}
                                selectedRawObj={selectedRawObj}
                                openDialog={openDialog}
                                />}
                            />
                            <Tab id="tr" title="Object Tree" panel={
                                <ObjectTree
                                    nodes={nodes}
                                    selectedNode={selectedNode}
                                    selectedRawObj={selectedRawObj}
                                    openDialog={openDialog}
                                />}
                            />
                            <Tab id="tbl" title="Object Table" panel={
                                <ObjectTable
                                    objs={objs}
                                    selectedRawObj={selectedRawObj}
                                    openDialog={openDialog}
                                />}
                            />                
                
                            <Tabs.Expander />
                
                        </Tabs>
                    </div>
                </div>
            </div>
       </Template>
    );
}

export default Detail;