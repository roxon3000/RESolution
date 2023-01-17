import React, { useEffect } from 'react';
import Template from './Template'
import Summary from './Summary'
import ObjectTree from './ObjectTree'
import { useSearchParams } from "react-router-dom";

function Detail(props) {

   let [searchParams, setSearchParams] = useSearchParams();
   let file = searchParams.get('file');

   return (
       <Template>
           <div className="container">
               <div className="row">
                   <div className="col">
                       <h1>Select File: {file}</h1>
                   </div>
               </div>
               <div className="row">
                   <div className="col">
                       <Summary></Summary>
                   </div>
               </div>
               <div className="row">
                   <div className="col">
                       <ObjectTree></ObjectTree>
                   </div>
               </div>

           </div>

       </Template>
    );
}

export default Detail;