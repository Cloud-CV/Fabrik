import React from 'react'
import data from './data'
import jsPlumbReady from './jsplumb'

var instance,_addLayerEndpoints;

var Layer = React.createClass({
    componentDidMount:function(){
        _addLayerEndpoints(this.props.id,data[this.props.type].endpoint.src,data[this.props.type].endpoint.trg);
    },
    componentWillUnmount:function(){
        console.log(this.props.id+" will get unmounted")
        instance.deleteEndpoint(this.props.id+"-s0");
        instance.deleteEndpoint(this.props.id+"-t0");
    },
    render: function() {
    	return <div className={"layer "+this.props.class} id={this.props.id} style={{top:this.props.top,left:this.props.left,background:data[this.props.type].color}} onClick={() => this.props.click(this.props.id)}>
        {data[this.props.type].name}
        </div>
  	}
})


var Canvas=React.createClass({
  	allowDrop: function(e) {
	    e.preventDefault();    
	},
    clickOrDragged:0,// whether a layer was clicked or dragged
	clickLayerEvent:function(id){// happens when layer is clicked and also dragged
		if(this.clickOrDragged==0){
			this.props.changeSelectedLayer(id) //clicked
		}
		else if(this.clickOrDragged==1){
			this.clickOrDragged=0 //dragged
		}
	},
    clickCanvas:function(e){
        if(e.target.id=='canvas'){
            this.props.changeSelectedLayer(null)
        }
    },
    updateLayerPosition:function(e){
        if(!this.clickOrDragged){
            this.clickOrDragged=1
        }
        var id=e.el.id
        var layer=this.props.net[id]
        layer.state.left=e.pos["0"]+'px'
        layer.state.top=e.pos["1"]+'px'
        this.props.modifyLayer(layer,id)
    },
  	componentDidUpdate:function(){
		instance.draggable(jsPlumb.getSelector(".layer"), {drag: this.updateLayerPosition});
	},
	componentDidMount:function(){
        var temp=jsPlumbReady()
        instance=temp.instance
        _addLayerEndpoints=temp._addLayerEndpoints

        instance.bind("connection",this.connectionEvent);
        
        instance.bind("connectionDetached", function (connInfo, originalEvent) {
                
        });
	},
    connectionEvent:function(connInfo, originalEvent){
        if(originalEvent!=null){//user manually makes a connection
            var src_id=connInfo.connection.sourceId
            var trg_id=connInfo.connection.targetId

            var layer_src=this.props.net[src_id]
            layer_src.connection.output=trg_id
            this.props.modifyLayer(layer_src,src_id)

            var layer_trg=this.props.net[trg_id]
            layer_trg.connection.input=src_id
            this.props.modifyLayer(layer_trg,trg_id)
        }
    },
	drop: function(e){
		e.preventDefault();
	 	var type = e.dataTransfer.getData("element_type");
	    var l={};
	    l['info']={type:type,color:data[type].color}
        l['state']={top:(e.clientY-e.target.offsetTop-100)+'px',left:(e.clientX-e.target.offsetLeft-30)+'px',class:''}
        //100px difference between layerTop and dropping point
        //30px difference between layerLeft and dropping point
        l['connection']={input:null,output:null}
        l['params']=JSON.parse(JSON.stringify(data[type].params))
        l['props']={name:{name:'Name',value:data[type].name+this.props.nextLayerId}}
        this.props.addNewLayer(l)    
	},
    render: function() {
  		var layers=[],net=this.props.net
  		for(var i in net){
            var layer=net[i]
  			layers.push(<Layer id={i} key={i} type={layer.info.type} class={layer.info.class} top={layer.state.top} left={layer.state.left} click={this.clickLayerEvent}></Layer>)
  		}
    	return <div className="col-md-7 canvas" id="canvas" onDragOver={this.allowDrop} onDrop={this.drop} onClick={this.clickCanvas}>
    		{layers}
   			</div>
    }
})

export default Canvas