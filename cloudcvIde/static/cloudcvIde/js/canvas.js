import React from 'react';
import data from './data';
import jsPlumbReady from './jsplumb';
import Layer from './layer';
import Error from './error';
import panZoom from './panZoom'

class Canvas extends React.Component {
  constructor(props) {
    super(props);
    this.allowDrop = this.allowDrop.bind(this);
    this.drop = this.drop.bind(this);
    this.clickCanvas = this.clickCanvas.bind(this);
    this.clickLayerEvent = this.clickLayerEvent.bind(this);
    // whether a layer was clicked or dragged
    this.clickOrDraggedLayer = 0;
    this.mouseState = null;
  }
  componentDidMount() {
    instance = jsPlumbReady();
    instance.bind('connection', this.connectionEvent.bind(this));
    instance.bind('connectionDetached', this.detachConnectionEvent.bind(this));
    this.mouseState = panZoom();
  }
  componentDidUpdate() {
    instance.draggable(jsPlumb.getSelector('.layer'),
      {
        drag: this.updateLayerPosition.bind(this),
        grid: [8, 8],
      }
    );
    if (this.props.rebuildNet) {
      const net = this.props.net;
      Object.keys(net).forEach(inputId => {
        const layer = net[inputId];
        if ((layer.info.phase === this.props.selectedPhase) || (layer.info.phase === null)) {
          const outputs = layer.connection.output;
          outputs.forEach(outputId => {
            if ((net[outputId].info.phase === this.props.selectedPhase) || (net[outputId].info.phase === null)) {
              instance.connect({
                uuids: [`${inputId}-s0`, `${outputId}-t0`],
                editable: true,
              });
            }
          });
        }
      });
      this.props.changeNetStatus(false);
      // instance.repaintEverything();
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
  clickCanvas(event) {
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
      const srcId = connInfo.connection.sourceId;
      const trgId = connInfo.connection.targetId;
      const layerSrc = this.props.net[srcId];
      const layerTrg = this.props.net[trgId];

      layerSrc.connection.output.push(trgId);
      this.props.modifyLayer(layerSrc, srcId);

      layerTrg.connection.input.push(srcId);
      this.props.modifyLayer(layerTrg, trgId);
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
        class: '',
      };
      // 25px difference between layerTop and dropping point
      // 45px difference between layerLeft and dropping point
      layer.connection = { input: [], output: [] };
      layer.params = {};
      Object.keys(data[type].params).forEach(j => {
        layer.params[j] = data[type].params[j].value;
      });
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

    Object.keys(net).forEach(layerId => {
      const layer = net[layerId];
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
      >
        {errors}
      <div
        id="jsplumbContainer"
        data-zoom="1"
        data-x="0"
        data-y="0"
      >
        {layers}
      </div>
      </div>
    );
  }
}

Canvas.propTypes = {
  nextLayerId: React.PropTypes.number,
  selectedPhase: React.PropTypes.number,
  net: React.PropTypes.object,
  modifyLayer: React.PropTypes.func,
  addNewLayer: React.PropTypes.func,
  changeSelectedLayer: React.PropTypes.func,
  rebuildNet: React.PropTypes.bool,
  changeNetStatus: React.PropTypes.func,
  addError: React.PropTypes.func,
  dismissError: React.PropTypes.func,
  error: React.PropTypes.array,
};

export default Canvas;
