import React, { useEffect } from 'react';
import Template from './Template';
import Summary from './Summary';
import ObjectTree from './ObjectTree';
import ObjectTable from './ObjectTable';
import { useSearchParams } from "react-router-dom";
import { getObjectTree } from '../services';
import { useDispatch, useSelector } from 'react-redux';

function Detail(props) {
    const dispatch = useDispatch();
    let [searchParams, setSearchParams] = useSearchParams();
    let nodes = useSelector((state) => state.objecttree.tree);
    let selectedNode = useSelector((state) => state.objecttree.selectedNode);
    let selectedRawObj = useSelector((state) => state.objecttree.selectedRawObj);
    let openDialog = useSelector((state) => state.objecttree.openDialog);
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
                       <Summary></Summary>
                   </div>
               </div>
               <div className="row">
                   <div className="col">
                        <ObjectTree
                            nodes={nodes}
                            selectedNode={selectedNode}
                            selectedRawObj={selectedRawObj}
                            openDialog={openDialog}
                        />
                   </div>
               </div>
               <div className="row">
                   <div className="col">
                        <ObjectTable
                            objs={objs}
                            selectedRawObj={selectedRawObj}
                            openDialog={openDialog}
                        />
                   </div>
               </div>
           </div>

       </Template>
    );
}

export default Detail;