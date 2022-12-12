import React from 'react';
import {getDetailData} from '../services';
import {connect} from 'react-redux';
import Template from './Template'

class Detail extends React.Component {																										
  
  constructor(props){
    super(props)
   
  }


  render() {
    var charts = this.props.charts

      return (				
        <Template>
              <div> Details - add something here</div>        
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
    charts: state,
    loading: state
  }
)

export default  connect(mapStateToProps, mapDispatchToProps) (Detail);