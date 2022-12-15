import React from 'react';
import '../css/template.css';

class Template extends React.Component {	
   
   render() {
     return (				
       <div className="container">
        <div className="row rounded banner">
          <div className="col-lg">
            <h1>RE Viewer UI</h1>
          </div>
        </div>
        <div className="row">
            <div className="col-sm">
                <a href="/" className="btn btn-primary">Home</a>
            </div>
            <div className="col-sm">
                <a href="/Detail" className="btn btn-primary">Detail</a>
            </div>
            <div className="col-sm">
                <a href="/exampletree" className="btn btn-primary">Example</a>
            </div>
        </div>
        {this.props.children}
      </div>
       
     );
   }
 }			
 
 export default Template;