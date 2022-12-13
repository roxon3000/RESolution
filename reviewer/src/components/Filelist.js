import React from 'react';
import Card from './Card';

class FileList extends React.Component {

    render() {
        var files = this.props.files;

        return (
            <div className="row">
                {
                    (files == null) || (files.map == undefined) ? "" : files.map(
                        (file) => <Card title={card.title} content={card.content} href={card.link} buttonContent={card.buttonContent} />
                    )
                }
            </div>
        );
    }
}

export default CardList;