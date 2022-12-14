import React from 'react';
import Card from './Card';

class CardList extends React.Component {

    render() {
        var cards = this.props.cards;

        return (
            <div className="row">
                {
                    (cards == null) || (cards.map == undefined) ? "" : cards.map(
                        (card) => <Card key={card.key}  title={card.name} content={card.desc} href={card.path} buttonContent={<div>Open</div>} />
                    )
                }
            </div>
        );
    }
}

export default CardList;

