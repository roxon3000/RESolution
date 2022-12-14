import React from 'react';
import {getDetailData} from '../services';
import {connect} from 'react-redux';
import Template from './Template'

class Detail extends React.Component {																										
  
  constructor(props){
    super(props)
   
  }


  render() {
    var tree = this.props.tree

      return (				
          <Template>
              <div> Detail - add something here</div>        

        </Template>
      
    );
  }
}				


const mapDispatchToProps = dispatch =>  {
  return {
    loadTrendData: () => {
          dispatch(getDetailData());
    }
  }
}

const mapStateToProps = state => 
(
  { 
    tree: state,
    loading: state
  }
)

export default  connect(mapStateToProps, mapDispatchToProps) (Detail);