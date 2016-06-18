import React from 'react';
import data from './data';
import jsPlumbReady from './jsplumb';
import Layer from './layer';

class Canvas extends React.Component {
  constructor(props) {
    super(props);
    this.allowDrop = this.allowDrop.bind(this);
    this.drop = this.drop.bind(this);
    this.clickCanvas = this.clickCanvas.bind(this);
    this.clickLayerEvent = this.clickLayerEvent.bind(this);
    this.clickOrDragged = 0;// whether a layer was clicked or dragged
  }
  componentDidMount() {
    const temp = jsPlumbReady();
    instance = temp.instance;
    addLayerEndpoints = temp.addLayerEndpoints;

    instance.bind('connection', this.connectionEvent.bind(this));

    /* instance.bind('connectionDetached', function (connInfo, originalEvent) {

    });*/
  }
  componentDidUpdate() {
    instance.draggable(jsPlumb.getSelector('.layer'),
      {
        drag: this.updateLayerPosition.bind(this),
        grid: [8, 8],
      }
    );
  }
  allowDrop(e) {
    e.preventDefault();
  }
  clickLayerEvent(id) { // happens when layer is clicked and also dragged
    if (this.clickOrDragged === 0) {
      this.props.changeSelectedLayer(id); // clicked
    } else if (this.clickOrDragged === 1) {
      this.clickOrDragged = 0; // dragged
    }
  }
  clickCanvas(e) {
    if (e.target.id === 'canvas') {
      this.props.changeSelectedLayer(null);
    }
  }
  updateLayerPosition(e) {
    if (!this.clickOrDragged) {
      this.clickOrDragged = 1;
    }
    const id = e.el.id;
    const layer = this.props.net[id];
    layer.state.left = `${e.pos['0']}px`;
    layer.state.top = `${e.pos['1']}px`;
    this.props.modifyLayer(layer, id);
  }
  connectionEvent(connInfo, originalEvent) {
    if (originalEvent != null) { // user manually makes a connection
      const srcId = connInfo.connection.sourceId;
      const trgId = connInfo.connection.targetId;
      const layerSrc = this.props.net[srcId];
      const layerTrg = this.props.net[trgId];

      layerSrc.connection.output = trgId;
      this.props.modifyLayer(layerSrc, srcId);

      layerTrg.connection.input = srcId;
      this.props.modifyLayer(layerTrg, trgId);
    }
  }
  drop(e) {
    e.preventDefault();
    const type = e.dataTransfer.getData('element_type');
    const l = {};
    l.info = { type, color: data[type].color };
    l.state = {
      top: `${e.clientY - e.target.offsetTop - 30}px`,
      left: `${e.clientX - e.target.offsetLeft - 65}px`,
      class: '',
    };
    // 30px difference between layerTop and dropping point
    // 65px difference between layerLeft and dropping point
    l.connection = { input: null, output: null };
    l.params = JSON.parse(JSON.stringify(data[type].params));
    l.props = {
      name: {
        name: 'Name',
        value: `${data[type].name}${this.props.nextLayerId}`,
        type: 'text',
      },
    };
    this.props.addNewLayer(l);
  }
  render() {
    const layers = [];
    const net = this.props.net;

    Object.keys(net).forEach(i => {
      const layer = net[i];
      layers.push(
        <Layer
          id={i} key={i}
          type={layer.info.type}
          class={layer.info.class}
          top={layer.state.top}
          left={layer.state.left}
          click={this.clickLayerEvent}
        />
      );
    });

    return (
      <div
        className="col-md-7 canvas"
        id="canvas"
        onDragOver={this.allowDrop}
        onDrop={this.drop}
        onClick={this.clickCanvas}
      >
        {layers}
      </div>
    );
  }
}

Canvas.propTypes = {
  nextLayerId: React.PropTypes.number,
  net: React.PropTypes.object,
  modifyLayer: React.PropTypes.func,
  addNewLayer: React.PropTypes.func,
  changeSelectedLayer: React.PropTypes.func,
};

export default Canvas;
