
import React from 'react';
import '../css/card.css';

class Card extends React.Component {

    render() {
        return (
            <div className="col-sm">
                <div className="card homeCard">
                    <div className="card-body">
                        <h5 className="card-title">{this.props.title}</h5>
                        <div className="card-text">{this.props.content}</div>
                        <a href={this.props.href} className="btn btn-primary">{this.props.buttonContent}</a>
                    </div>
                </div>
            </div>
        );
    }
}

export default Card;

