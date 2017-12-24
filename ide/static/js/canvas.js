import React from 'react';
import data from './data';
import jsPlumbReady from './jsplumb';
import Layer from './layer';
import Error from './error';
import panZoom from './panZoom';
import $ from 'jquery'

class Canvas extends React.Component {
  constructor(props) {
    super(props);
    this.allowDrop = this.allowDrop.bind(this);
    this.drop = this.drop.bind(this);
    this.scrollCanvas = this.scrollCanvas.bind(this);
    this.clickCanvas = this.clickCanvas.bind(this);
    this.clickLayerEvent = this.clickLayerEvent.bind(this);
    this.hoverLayerEvent = this.hoverLayerEvent.bind(this);
    // whether a layer was clicked or dragged
    this.clickOrDraggedLayer = 0;
    this.hover = 0;
    this.mouseState = null;
    this.placeholder = true;
  }
  /* this function returns the layers between a specified output y and input y
  it also sneaks in another functionallity of determining which direction is most crowded. this is specifically 
  implemented in this function becuase performance will be very low if implemented in another loop.  */
  getBetween(net, output, input, x) {
    var toReturn = [];
    var neg = 0;
    var pos = 0;
    Object.keys(net).forEach(node => {
      var pos = [[net[node]['state']['left'], net[node]['state']['top']]]
      Object.keys(pos).forEach(function (row) {
        Object.keys(pos[row]).forEach(function (coord) {
          pos[row][coord] = parseInt(pos[row][coord].substring(0, pos[row][coord].length - 2));
        });
      });
      if (input < pos[0][1] && pos[0][1] < output) {
        toReturn.push(node);
        if (pos[0][0] > x) {neg++;} else{ pos++;}
      }
    });
    var dir = 0;
    if (neg>pos) dir = -1; else dir = 1; 
    return [dir, toReturn];
  }
  /* this function takes in a var of net and pos
  net has an array of all the nodes, and pos is a array of x and y coordinates that this 
  function checks to see whether a line will cut through nodes in the pathway.
  */
  checkIfCuttingLine(net, pos) {
    var between = this.getBetween(net, pos[0][1], pos[1][1], pos[0][0]);
    var dir = between[0];
    between = between[1];
    //slope is calculated for the line so it can form an equation for it.
    var slope = (pos[0][1] - pos[1][1]) / (pos[0][0] - pos[1][0] + dir);
    for (var i = 0; i < between.length; i++) {
      var checkingNet = between[i];
      if ((net[checkingNet].info.phase === this.props.selectedPhase) || (net[checkingNet].info.phase === null)) {
        var y = net[checkingNet]['state']['top'].substring(0, net[checkingNet]['state']['top'].length - 2);
        var x = net[checkingNet]['state']['left'].substring(0, net[checkingNet]['state']['left'].length - 2);
        //point slope equation is used to form xcalc. xcalc is the position te line will be at for a specified y coord.
        var xcalc = ((y - pos[1][1]) / slope) + pos[1][0];
        if (Math.abs(x - xcalc) < 100) {
          var extend = x - xcalc;
          //the following code is used for positioning the direction of the line and the while loop controling the function iteslf. 
          if (extend < 0) {
            return 1;
          }
          else {
            return -1;
          }
        }
      }
    }
    return 0;
  }
  /* the following code combines the previous functions and loops through output and input nodes and does a checkIfCuttingLine
  it while loops over checkcutting net untill the line is no longer cutting through a node. it could very possibly infinite, but
  chances of that are very slim, as long as there is a little empty space on the canvas, the code should be fine.  */
  checkCutting(net) {
    Object.keys(net).forEach(inputId => {
      const input = net[inputId];
      if ((input.info.phase === this.props.selectedPhase) || (input.info.phase === null)) {
        const outputs = input.connection.output;
        outputs.forEach(outputId => {
          if (outputId != "l1" && typeof net[outputId]['state']['left'] != "undefined") {
            const output = net[outputId];
            var pos = [[output['state']['left'], output['state']['top']], [input['state']['left'], input['state']['top']]]
            Object.keys(pos).forEach(function (row) {
              Object.keys(pos[row]).forEach(function (coord) {
                pos[row][coord] = parseInt(pos[row][coord].substring(0, pos[row][coord].length - 2));
              });

            });
            var extend = 0;
            var direction = this.checkIfCuttingLine(net,pos);
            while(this.checkIfCuttingLine(net,pos) != 0) {
              extend += 80*direction;
              pos[0][0] += 70*direction;
              pos[1][0] += 70*direction;
            }
          }
          if ((net[outputId].info.phase === this.props.selectedPhase) || (net[outputId].info.phase === null)) {
            window.connectorParams = window.connectorParams || {};
            window.connectorParams[inputId] = window.connectorParams[inputId] || {};
            //if (Math.abs(window.connectorParams[inputId][outputId]) < Math.abs(extend)) {
            window.connectorParams[inputId][outputId] = extend;
            //}
          }
        });
      }
    });
  }
  componentDidMount() {
    this.placeholder = false;
    instance = jsPlumbReady();
    instance.bind('connection', this.connectionEvent.bind(this));
    instance.bind('connectionDetached', this.detachConnectionEvent.bind(this));
    this.mouseState = panZoom();
  }
  componentDidUpdate() {
    this.placeholder = false;
    instance.draggable(jsPlumb.getSelector('.layer'),
      {
        drag: this.updateLayerPosition.bind(this),
        grid: [8, 8]
      }
    );
    const net = this.props.net;    
    if (this.props.rebuildNet) {
      let combined_layers = ['ReLU', 'LRN', 'TanH', 'BatchNorm', 'Dropout', 'Scale'];
      this.checkCutting(net);
      Object.keys(net).forEach(inputId => {
        const layer = net[inputId];
        if ((layer.info.phase === this.props.selectedPhase) || (layer.info.phase === null)) {
          const outputs = layer.connection.output;
          outputs.forEach(outputId => {
            if ((net[outputId].info.phase === this.props.selectedPhase) || (net[outputId].info.phase === null)) {
              instance.connect({
                uuids: [`${inputId}-s0`, `${outputId}-t0`],
                editable: true
              });
              /* The following code is to identify layers that are part of a group
              and modify their border radius */
              if ($.inArray(net[outputId].info.type, combined_layers) != -1 &&net[inputId].connection.output.length==1){
                if ($.inArray(net[inputId].info.type, combined_layers) == -1){
                  $('#'+inputId).css('border-radius', '10px 10px 0px 0px')
                }
                else {
                  $('#'+inputId).css('border-radius', '0px 0px 0px 0px')
                }
              }
              else if (net[inputId].connection.input.length==1){
                if ($.inArray(net[inputId].info.type, combined_layers) != -1){
                  $('#'+inputId).css('border-radius', '0px 0px 10px 10px')
                }
              }
            }
          });
        }
      });
      this.props.changeNetStatus(false);
      // instance.repaintEverything();
    }
    // Might need to improve the logic of clickEvent
    if(Object.keys(net).length>1 && this.props.clickEvent){
      for (let i = this.props.nextLayerId - 1; i >= 0; i --) { //find last layer id
        if (net[`l${i}`] !== undefined) {
          var lastLayerId = i;
          break;
        }
      }
      for (let i = lastLayerId - 1; i >= 0; i --) { //find second last layer id
        if (net[`l${i}`] !== undefined) {
          var prevLayerId = i;
          break;
        }
      }
      lastLayerId = `l${lastLayerId}`; //add 'l' ahead of the index
      prevLayerId = `l${prevLayerId}`;
      const x1 = parseInt(net[prevLayerId].state.top.split('px'));
      const x2 = parseInt(net[lastLayerId].state.top.split('px')); 
      const s = instance.getEndpoints(prevLayerId)[0];
      var t = instance.getEndpoints(lastLayerId);
      // To handle case of loss layer being target
      if (t.length == 1){
        t = t[0];
      }
      else{
        t = t[1];
      }
      if (x2-x1==80) { //since only layers added through handleClick will be exactly 80px apart, we can connect those like this.
        instance.connect({
          source: s,
          target: t});
      }
    }
  }
  allowDrop(event) {
    event.preventDefault();
  }
  clickLayerEvent(event, layerId) { // happens when layer is clicked and also dragged
    if (this.clickOrDraggedLayer === 0) {
      this.props.changeSelectedLayer(layerId); // clicked
    } else if (this.clickOrDraggedLayer === 1) {
      this.clickOrDraggedLayer = 0; // dragged
    }
    event.stopPropagation();
  }
  hoverLayerEvent(event, layerId) { // happens when layer is hovered
    if (this.hover === 0) {
      this.props.changeHoveredLayer(layerId);
    } else if (this.hover === 1) {
      this.hover = 0;
    }
    event.stopPropagation();
  }
  scrollCanvas() {
    $('#netName').css('top', '-' + $('#panZoomContainer').scrollTop() + 'px');
  }
  clickCanvas(event) {
    this.placeholder = false;
    event.preventDefault();
    if (event.target.id === 'panZoomContainer' && !this.mouseState.pan) {
      this.props.changeSelectedLayer(null);
    }
    this.mouseState.pan = false;
    this.mouseState.click = false;
    event.stopPropagation();
  }
  updateLayerPosition(event) {
    if (!this.clickOrDraggedLayer) {
      this.clickOrDraggedLayer = 1;
    }
    const layerId = event.el.id;
    const layer = this.props.net[layerId];
    layer.state.left = `${event.pos['0']}px`;
    layer.state.top = `${event.pos['1']}px`;
    this.props.modifyLayer(layer, layerId);
    let net = this.props.net  
    this.checkCutting(net);  
  }
  connectionEvent(connInfo, originalEvent) {
    if (originalEvent != null) { // user manually makes a connection
      /* Added check for cyclic graphs, the custom BFS finds all parents
      of the source node and then checks to see if the target matches
      any parent*/
      var parents = [];
      var stack = [connInfo.connection.sourceId];
      var targetIsParent = false;
      const srcId = connInfo.connection.sourceId;
      const trgId = connInfo.connection.targetId;
      const layerSrc = this.props.net[srcId];
      const layerTrg = this.props.net[trgId];
      while (stack.length!=0){
        for(var i=0; i<this.props.net[stack[0]].connection.input.length; i++){
          stack.push(this.props.net[stack[0]].connection.input[i]);
        }
        parents.push(stack.shift());
      }
      for (i=0; i<parents.length; i++)
        if (parents[i] == trgId){
          targetIsParent = true;
          break;
        }
      if (targetIsParent == true || srcId==trgId)
        this.props.addError(`Error: cyclic graphs are not allowed`);
      else{
        layerSrc.connection.output.push(trgId);
        this.props.modifyLayer(layerSrc, srcId);

        layerTrg.connection.input.push(srcId);
        this.props.modifyLayer(layerTrg, trgId);
      }
    }
  }
  detachConnectionEvent(connInfo, originalEvent) {
    if (originalEvent != null) { // user manually detach a connection
      const srcId = connInfo.connection.sourceId;
      const trgId = connInfo.connection.targetId;
      const layerSrc = this.props.net[srcId];
      const layerTrg = this.props.net[trgId];
      let index;

      index = layerSrc.connection.output.indexOf(trgId);
      layerSrc.connection.output.splice(index, 1);
      this.props.modifyLayer(layerSrc, srcId);

      index = layerTrg.connection.input.indexOf(srcId);
      layerTrg.connection.input.splice(index, 1);
      this.props.modifyLayer(layerTrg, trgId);
    }
  }
  drop(event) {
    this.placeholder = false;
    event.preventDefault();
    const canvas = document.getElementById('jsplumbContainer');
    const zoom = instance.getZoom();

    const type = event.dataTransfer.getData('element_type');
    if (data[type].learn && (this.props.selectedPhase === 1)) {
      this.props.addError(`Error: you can not add a "${type}" layer in test phase`);
    } else {
      const layer = {};
      let phase = this.props.selectedPhase;

      // a layer added in train phase is common
      if (phase === 0) {
        phase = null;
      }

      layer.info = { type, phase };
      layer.state = {
        top: `${(event.clientY - event.target.getBoundingClientRect().top - canvas.y + $('#panZoomContainer').scrollTop())/zoom - 25}px`,
        left: `${(event.clientX - event.target.getBoundingClientRect().left - canvas.x + $('#panZoomContainer').scrollLeft())/zoom - 45}px`,
        class: ''
      };
      // 25px difference between layerTop and dropping point
      // 45px difference between layerLeft and dropping point
      layer.connection = { input: [], output: [] };
      layer.params = {};
      Object.keys(data[type].params).forEach(j => {
        layer.params[j] = [data[type].params[j].value, false];
      });

      layer.params['endPoint'] = [data[type]['endpoint'], false];
      // l.props = JSON.parse(JSON.stringify(data[type].props));
      layer.props = {};
      // default name
      layer.props.name = `${data[type].name}${this.props.nextLayerId}`;
      this.props.addNewLayer(layer);
    }
  }
  render() {
    const layers = [];
    const errors = [];
    const net = this.props.net;
    const error = this.props.error;
    let placeholder = null;
    if (this.placeholder){
      placeholder = (<h4 className="text-center" id="placeholder">Load an existing model from the folder dropdown</h4>)
    }
    Object.keys(net).forEach(layerId => {
      const layer = net[layerId];
      if (layer.info.type == 'Python'){
        // Changing endpoints depending on the type of Python layer
        if (layer.params.endPoint[0] == '1, 0'){
          data[layer.info.type]['endpoint']['trg'] = [];
          data[layer.info.type]['endpoint']['src'] = ['Bottom'];
        }
        else if (layer.params.endPoint[0] == '0, 1'){
          data[layer.info.type]['endpoint']['trg'] = ['Top'];
          data[layer.info.type]['endpoint']['src'] = [];
        }
        else{
          data[layer.info.type]['endpoint']['trg'] = ['Top'];
          data[layer.info.type]['endpoint']['src'] = ['Bottom'];
        }
        if (layer.params){
          Object.keys(layer.params).forEach(param => {
            if (param != 'endPoint'){
            data[layer.info.type]['params'][param] = {'name': param, 'type': 'text',
            'required': false, 'value': ''};
            }
          });
        }

      }
      if ((layer.info.phase === this.props.selectedPhase) || (layer.info.phase === null)) {
        layers.push(
          <Layer
            id={layerId}
            key={layerId}
            type={layer.info.type}
            class={layer.info.class}
            top={layer.state.top}
            left={layer.state.left}
            click={this.clickLayerEvent}
            hover={this.hoverLayerEvent}

          />
        );
      }
    });

    error.forEach((errorText, errorIndex) => {
      errors.push(
        <Error
          text={errorText}
          key={errorIndex}
          index={errorIndex}
          dismissError={this.props.dismissError}
        />
      );
    });

    return (
      <div
        className="canvas"
        id="panZoomContainer"
        onDragOver={this.allowDrop}
        onDrop={this.drop}
        onClick={this.clickCanvas}
        onScroll={this.scrollCanvas}
      >
        {errors}
        {placeholder}
      <div
        id="jsplumbContainer"
        data-zoom="1"
        data-x="0"
        data-y="0"
      >
        {layers}
      </div>
      <div id='modelParameter'>
        <p>Total Parameters</p>
        <div id="content">
          {this.props.totalParameters}
        </div>
      </div>
      <div id='icon-plus' className="canvas-icon">
        <p>Press ]</p>
        <button className="btn btn-default text-center">
            <span className="glyphicon glyphicon glyphicon-plus" aria-hidden="true"></span>
        </button>
      </div>
      <div id='icon-minus' className="canvas-icon">
        <p>Press [</p>
        <button className="btn btn-default text-center">
            <span className="glyphicon glyphicon glyphicon-minus" aria-hidden="true"></span>
        </button>
      </div>
      </div>
    );
  }
}

Canvas.propTypes = {
  nextLayerId: React.PropTypes.number,
  selectedPhase: React.PropTypes.number,
  net: React.PropTypes.object.isRequired,
  modifyLayer: React.PropTypes.func,
  addNewLayer: React.PropTypes.func,
  changeSelectedLayer: React.PropTypes.func,
  changeHoveredLayer: React.PropTypes.func,
  rebuildNet: React.PropTypes.bool,
  changeNetStatus: React.PropTypes.func,
  addError: React.PropTypes.func,
  dismissError: React.PropTypes.func,
  error: React.PropTypes.array,
  placeholder: React.PropTypes.bool,
  clickEvent: React.PropTypes.bool,
  totalParameters: React.PropTypes.number
};

export default Canvas;
