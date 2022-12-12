import React from 'react';
import {getHomeData} from '../services';
import { connect } from 'react-redux';
import Template from './Template'


class Home extends React.Component {	
   constructor(props){
     super(props);
     this.props.loadHomeData();
   }

  render() {
      return (		
        <Template>
              <div>
                  Home  - add something here
              </div>
              
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
    cards: state
  }
);


export default connect(mapStateToProps, mapDispatchToProps)(Home);