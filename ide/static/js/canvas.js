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
      const x1 = parseInt(net[`l${this.props.nextLayerId-2}`].state.top.split('px'));
      const x2 = parseInt(net[`l${this.props.nextLayerId-1}`].state.top.split('px')); 
      const s = instance.getEndpoints(`l${this.props.nextLayerId-2}`)[0];
      var t = instance.getEndpoints(`l${this.props.nextLayerId-1}`);
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
        top: `${(event.clientY - event.target.getBoundingClientRect().top - canvas.y)/zoom - 25}px`,
        left: `${(event.clientX - event.target.getBoundingClientRect().left - canvas.x)/zoom - 45}px`,
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
