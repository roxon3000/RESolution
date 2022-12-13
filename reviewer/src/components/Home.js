import React from 'react';
import {getHomeData} from '../services';
import { connect } from 'react-redux';
import Template from './Template'
import CardList from './CardList'

class Home extends React.Component {	
   constructor(props){
     super(props);
       this.props.loadHomeData();
     
   }

  render() {
      return (		
        <Template>
              <div className="row">
                  <div className="col-md">Files For Reverse Engineering Analysis</div>
              </div>
              <CardList cards={this.props.files} />
        </Template>
      
    );
  }
}																																																																																																											

const mapDispatchToProps = dispatch =>  {
  return {
    loadHomeData: () => {
      dispatch(getHomeData());
    }
  };
};

const mapStateToProps = state => 
(
  { //todo update this to new structure
    files: state.pdfreducer.files
  }
);


export default connect(mapStateToProps, mapDispatchToProps)(Home);