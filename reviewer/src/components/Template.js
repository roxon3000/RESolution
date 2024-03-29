import React from 'react';
import '../css/template.css';

function Template(props) {

    return (
        <div className="container, template">
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
                    
                </div>
                <div className="col-sm">
                    
                </div>
            </div>
            <div style={{ marginTop: "10px" }} ></div>
            {props.children}
        </div>

    );
}

export default Template;