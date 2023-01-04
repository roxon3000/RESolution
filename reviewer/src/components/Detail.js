import React, { useEffect } from 'react';
import Template from './Template'
import Summary from './Summary'
import ObjectTree from './ObjectTree'
function Detail(props) {

   return (
       <Template>
           <div className="container">
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