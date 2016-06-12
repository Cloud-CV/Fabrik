import React from 'react'
import Canvas from './canvas'
import Pane from './pane'
import SetParams from './setParams'

export default React.createClass({
  getInitialState: function() {
  	return {net:{},selectedLayer:null,nextLayerId:0};
	},
  addNewLayer:function(l){
  	var net=this.state.net;
  	net["l"+this.state.nextLayerId]=l
    this.setState({net:net,nextLayerId:this.state.nextLayerId+1});
    
  },
  changeSelectedLayer:function(n){
    var net=this.state.net;
    if(this.state.selectedLayer){
      net[this.state.selectedLayer].info.class='' //remove css from previously selected layer
    }
    if(n){
      net[n].info.class='selected'  //css when layer is selected
    }
		this.setState({net:net,selectedLayer:n});
  },
  modifyLayer:function(l,id=this.state.selectedLayer){
    var net=this.state.net;
    net[id]=l
    this.setState({net:net})
    console.log(this.state.net)
  },
  deleteLayer:function(){
    var net=this.state.net;
    var id=this.state.selectedLayer
    var input_id=net[id].connection.input
    var output_id=net[id].connection.output
    delete net[id]
    if(input_id){
      net[input_id].connection.output=null
    }
    if(output_id){
      net[output_id].connection.input=null
    }
    this.setState({net:net,selectedLayer:null})
  },
  render: function(){
    return  <div className="container-fluid">
              <div className="content row">
                <Pane></Pane>
		            <Canvas net={this.state.net} addNewLayer={this.addNewLayer} nextLayerId={this.state.nextLayerId} changeSelectedLayer={this.changeSelectedLayer} modifyLayer={this.modifyLayer}></Canvas>
                <SetParams net={this.state.net} selectedLayer={this.state.selectedLayer} modifyLayer={this.modifyLayer} deleteLayer={this.deleteLayer}></SetParams>		    
		          </div>
            </div>
	}
})


