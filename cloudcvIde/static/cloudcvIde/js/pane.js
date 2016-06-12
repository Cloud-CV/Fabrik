import React from 'react'


var PaneElement = React.createClass({
  drag:function(e){
	e.dataTransfer.setData("element_type",e.target.id);
  },
  render:function(){
    return <div className="btn btn-default btn-block" draggable="true" onDragStart={this.drag} id={this.props.id}>{this.props.children}</div>
  }
});

var Pane = React.createClass({
  render:function(){
	return 	<div className="col-md-2 pane">
	    	  <PaneElement id="input">Input</PaneElement>
	    	  <PaneElement id="conv">Convolution</PaneElement>
	          <PaneElement id="maxpool">Max pooling</PaneElement>
	    	  <PaneElement id="relu">ReLU</PaneElement>
	    	  <PaneElement id="fc">FC</PaneElement>
	    	  <PaneElement id="output">Output</PaneElement>
			</div>
  }
});

export default Pane