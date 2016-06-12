import React from 'react'

var Field = React.createClass({
  change:function(e){
    this.props.changeParams(this.props.id,e.target.value)
  },
  render: function() {
    return  <div className="form-group">
              <label htmlFor={this.props.id} className="col-sm-5 control-label">{this.props.label}</label>
              <div className="col-sm-7">
                <input type="text" value={this.props.value} className="form-control" id={this.props.id} onChange={this.change}/>
              </div>
            </div>
  }
})

export default React.createClass({
	changeProps:function(prop,value){
    var net=this.props.net
    var layer=net[this.props.selectedLayer]
    layer.props[prop].value=value
    this.props.modifyLayer(layer)
	},
  changeParams:function(para,value){
    var net=this.props.net
    var layer=net[this.props.selectedLayer]
    layer.params[para].value=value
    this.props.modifyLayer(layer)
  },
  render:function(){
    if(this.props.selectedLayer){
      var params=[]
      var props=[]
      var layer=this.props.net[this.props.selectedLayer]
    
      for(var i in layer.params){
        params.push(<Field id={i} key={i} label={layer.params[i].name} value={layer.params[i].value} changeParams={this.changeParams}></Field>)
      }
      for(var i in layer.props){
        props.push(<Field id={i} key={i} label={layer.props[i].name} value={layer.props[i].value} changeParams={this.changeProps}></Field>)
      }
      
      return  <div className="col-md-3 setparams" >
                <div className="setHead" style={{color:layer.info.color}}>{layer.props.name.value} layer selected</div>
                <div className="setContain">
                  <form className="form-horizontal">
                    Properties
                    {props}
                  </form>
                  <br/>
                  <form className="form-horizontal">
                    Parameters
                    {params}
                  </form>
        
                  <button type="button" className="btn btn-danger" style={{marginLeft:'80px',marginTop:'50px'}} onClick={this.props.deleteLayer}>Delete this layer</button>
        	     </div>
              </div>
    }
    else{
    	return  <div className="col-md-3 setparams" >
                <div className="setHead" style={{color:'white'}}>Settings</div>
                <div style={{padding:'30px'}}>select a layer to set its parameters</div>
    	        </div>
    }
  }
})