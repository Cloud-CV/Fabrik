import React from 'react';
import Canvas from './canvas';
import Pane from './pane';
import SetParams from './setParams';
import TopBar from './topBar';

class Content extends React.Component {
  constructor(props) {
    super(props);
    this.state = { net: {}, selectedLayer: null, nextLayerId: 0 };
    this.addNewLayer = this.addNewLayer.bind(this);
    this.changeSelectedLayer = this.changeSelectedLayer.bind(this);
    this.modifyLayer = this.modifyLayer.bind(this);
    this.deleteLayer = this.deleteLayer.bind(this);
    this.exportNet = this.exportNet.bind(this);
  }
  addNewLayer(l) {
    const net = this.state.net;
    net[`l${this.state.nextLayerId}`] = l;
    this.setState({ net, nextLayerId: this.state.nextLayerId + 1 });
  }
  changeSelectedLayer(n) {
    const net = this.state.net;
    if (this.state.selectedLayer) {
      // remove css from previously selected layer
      net[this.state.selectedLayer].info.class = '';
    }
    if (n) {
      // css when layer is selected
      net[n].info.class = 'selected';
    }
    this.setState({ net, selectedLayer: n });
  }
  modifyLayer(l, id = this.state.selectedLayer) {
    const net = this.state.net;
    net[id] = l;
    this.setState({ net });
  }
  deleteLayer() {
    const net = this.state.net;
    const id = this.state.selectedLayer;
    const inputId = net[id].connection.input;
    const outputId = net[id].connection.output;
    delete net[id];
    if (inputId) {
      net[inputId].connection.output = null;
    }
    if (outputId) {
      net[outputId].connection.input = null;
    }
    this.setState({ net, selectedLayer: null });
  }
  exportNet() {
    $.ajax({
      url: '/cloudcvide/export',
      dataType: 'json',
      type: 'POST',
      data: {
        net: JSON.stringify(this.state.net),
      },
      success(data) {
        // only for demo purpose - will be removed later
        document.getElementById('prototxt').innerHTML = data.result;
        $('html, body').animate(
          { scrollTop: $('#prototxt').offset().top },
          'slow'
        );
      },
      error() {
        // only for demo purpose - will be removed later
        document.getElementById('prototxt').innerHTML = '<b style="color:red;">failure</b>';
        $('html, body').animate(
          { scrollTop: $('#prototxt').offset().top },
          'slow'
        );
      },
    });
  }
  render() {
    return (
      <div className="container-fluid">
        <TopBar exportNet={this.exportNet} />
        <div className="content row">
          <Pane />
          <Canvas
            net={this.state.net}
            addNewLayer={this.addNewLayer}
            nextLayerId={this.state.nextLayerId}
            changeSelectedLayer={this.changeSelectedLayer}
            modifyLayer={this.modifyLayer}
          />
          <SetParams
            net={this.state.net}
            selectedLayer={this.state.selectedLayer}
            modifyLayer={this.modifyLayer}
            deleteLayer={this.deleteLayer}
          />
        </div>
      </div>
    );
  }
}

export default Content;
