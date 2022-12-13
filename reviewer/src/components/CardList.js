import React from 'react';
import Card from './Card';

class CardList extends React.Component {

    render() {
        var cards = this.props.cards;

        return (
            <div className="row">
                {
                    (cards == null) || (cards.map == undefined) ? "" : cards.map(
                        (card) => <Card title={card.name} content={<div>test</div>} href={card.path} buttonContent={<div>Open</div>} />
                    )
                }
            </div>
        );
    }
}

export default CardList;

