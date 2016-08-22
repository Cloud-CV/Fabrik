import React from 'react';
import Canvas from './canvas';
import Pane from './pane';
import SetParams from './setParams';
import TopBar from './topBar';
import Tabs from './tabs';
import data from './data';
import netLayout from './netLayout';

class Content extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      net: {},
      net_name: null,
      selectedLayer: null,
      nextLayerId: 0,
      rebuildNet: false,
      selectedPhase: 0,
      error: [],
      load: false,
    };
    this.addNewLayer = this.addNewLayer.bind(this);
    this.changeSelectedLayer = this.changeSelectedLayer.bind(this);
    this.modifyLayer = this.modifyLayer.bind(this);
    this.modifyLayerParams = this.modifyLayerParams.bind(this);
    this.deleteLayer = this.deleteLayer.bind(this);
    this.exportNet = this.exportNet.bind(this);
    this.importNet = this.importNet.bind(this);
    this.changeNetStatus = this.changeNetStatus.bind(this);
    this.changeNetPhase = this.changeNetPhase.bind(this);
    this.dismissError = this.dismissError.bind(this);
    this.addError = this.addError.bind(this);
    this.dismissAllErrors = this.dismissAllErrors.bind(this);
    this.copyTrain = this.copyTrain.bind(this);
    this.trainOnly = this.trainOnly.bind(this);
  }
  addNewLayer(layer) {
    const net = this.state.net;
    net[`l${this.state.nextLayerId}`] = layer;
    this.setState({ net, nextLayerId: this.state.nextLayerId + 1 });
  }
  changeSelectedLayer(layerId) {
    const net = this.state.net;
    if (this.state.selectedLayer) {
      // remove css from previously selected layer
      net[this.state.selectedLayer].info.class = '';
    }
    if (layerId) {
      // css when layer is selected
      net[layerId].info.class = 'selected';
    }
    this.setState({ net, selectedLayer: layerId });
  }
  modifyLayer(layer, layerId = this.state.selectedLayer) {
    const net = this.state.net;
    net[layerId] = layer;
    this.setState({ net });
  }
  modifyLayerParams(layer, layerId = this.state.selectedLayer) {
    const net = this.state.net;
    let index;

    if (this.state.selectedPhase === 1 && net[layerId].info.phase === null) {
      // we need to break this common layer for each phase
      const testLayer = JSON.parse(JSON.stringify(layer));
      const trainLayer = JSON.parse(JSON.stringify(net[layerId]));

      testLayer.info.phase = 1;
      (testLayer.connection.output).forEach(outputId => {
        if (net[outputId].info.phase === 0) {
          index = testLayer.connection.output.indexOf(outputId);
          testLayer.connection.output.splice(index, 1);
          index = net[outputId].connection.input.indexOf(layerId);
          net[outputId].connection.input.splice(index, 1);
        }
      });
      (testLayer.connection.input).forEach(inputId => {
        if (net[inputId].info.phase === 0) {
          index = testLayer.connection.input.indexOf(inputId);
          testLayer.connection.input.splice(index, 1);
          index = net[inputId].connection.output.indexOf(layerId);
          net[inputId].connection.output.splice(index, 1);
        }
      });
      net[layerId] = testLayer;
      this.setState({ net });

      trainLayer.info.phase = 0;
      trainLayer.props.name = `${data[trainLayer.info.type].name}${this.state.nextLayerId}`;
      (trainLayer.connection.output).forEach(outputId => {
        if (net[outputId].info.phase === 1) {
          index = trainLayer.connection.output.indexOf(outputId);
          trainLayer.connection.output.splice(index, 1);
        }
      });
      (trainLayer.connection.input).forEach(inputId => {
        if (net[inputId].info.phase === 1) {
          index = trainLayer.connection.input.indexOf(inputId);
          trainLayer.connection.input.splice(index, 1);
        }
      });

      const nextLayerId = `l${this.state.nextLayerId}`;

      (trainLayer.connection.output).forEach(outputId => {
        net[outputId].connection.input.push(nextLayerId);
      });

      (trainLayer.connection.input).forEach(inputId => {
        net[inputId].connection.output.push(nextLayerId);
      });

      this.addNewLayer(trainLayer);
    } else {
      net[layerId] = layer;
      this.setState({ net });
    }
  }
  deleteLayer(layerId) {
    const net = this.state.net;
    const input = net[layerId].connection.input;
    const output = net[layerId].connection.output;
    let index;
    delete net[layerId];
    input.forEach(inputId => {
      index = net[inputId].connection.output.indexOf(layerId);
      net[inputId].connection.output.splice(index, 1);
    });
    output.forEach(outputId => {
      index = net[outputId].connection.input.indexOf(layerId);
      net[outputId].connection.input.splice(index, 1);
    });
    this.setState({ net, selectedLayer: null });
  }
  exportNet(framework) {
    this.dismissAllErrors();
    const error = [];
    const net = this.state.net;

    Object.keys(net).forEach(layerId => {
      const layer = net[layerId];
      Object.keys(layer.params).forEach(param => {
        const paramData = data[layer.info.type].params[param];
        if (paramData.required === true && layer.params[param] === '') {
          error.push(`Error: "${paramData.name}" required in "${layer.props.name}" Layer`);
        }
      });
    });

    if (error.length) {
      this.setState({ error });
    } else {
      const netData = JSON.parse(JSON.stringify(this.state.net));
      Object.keys(netData).forEach(layerId => {
        delete netData[layerId].state;
      });

      const url = {'caffe': '/caffe/export', 'tensorflow': '/tensorflow/export'}
      this.setState({ load: true });
      $.ajax({
        url: url[framework],
        dataType: 'json',
        type: 'POST',
        data: {
          net: JSON.stringify(netData),
          net_name: this.state.net_name,
        },
        success : function (response) {
          if (response.result == 'success') {
            const downloadAnchor = document.getElementById('download');
            downloadAnchor.download = response.name;
            downloadAnchor.href = response.url;
            downloadAnchor.click();
          } else if (response.result == 'error') {
            this.addError(response.error);
          }
          this.setState({ load: false });
        }.bind(this),
        error() {
          // console.log('failure in exporting');
          this.setState({ load: false });
        },
      });
    }
  }
  importNet(framework) {
    this.dismissAllErrors();
    const formData = new FormData();
    formData.append('file', $('#inputFile'+framework)[0].files[0]);
    const url = {'caffe': '/caffe/import', 'tensorflow': '/tensorflow/import'};
    this.setState({ load: true });
    $.ajax({
      url: url[framework],
      dataType: 'json',
      type: 'POST',
      data: formData,
      processData: false,  // tell jQuery not to process the data
      contentType: false,
      success: function (response) {
        if (response.result === 'success'){
          this.initialiseImportedNet(response.net,response.net_name);
        } else if (response.result === 'error'){
          this.addError(response.error);
        }
        this.setState({ load: false });
      }.bind(this),
      error() {
        // console.log('failure');
        this.setState({ load: false });
      },
    });
  }
  initialiseImportedNet(net,net_name) {
    // this line will unmount all the layers
    // so that the new imported layers will all be mounted again
    const tempError = {};
    const error = [];
    this.setState({ net: {}, selectedLayer: null, nextLayerId: 0, selectedPhase: 0, error: [] });
    Object.keys(net).forEach(layerId => {
      const layer = net[layerId];
      const type = layer.info.type;
      const index = +layerId.substring(1);
      if (data.hasOwnProperty(type)) {
        // add the missing params with default values
        Object.keys(data[type].params).forEach(param => {
          if (!layer.params.hasOwnProperty(param)) {
            layer.params[param] = data[type].params[param].value;
          }
        });
        // layer.props = JSON.parse(JSON.stringify(data[type].props));
        layer.props = {};
        // default name
        layer.props.name = layerId;
      } else {
        tempError[type] = null;
      }
    });

    // initialize the position of layers
    let positions = netLayout(net);
    Object.keys(positions).forEach(layerId => {
      const layer = net[layerId];
      layer.state = {
        top: `${250 + 50 * positions[layerId][1]}px`,
        left: `${20 + 180 * positions[layerId][0]}px`,
        class: '',
      };
    });

    if (Object.keys(tempError).length) {
      Object.keys(tempError).forEach(type => {
        error.push(`Error: Currently we do not support prototxt with "${type}" Layer.`);
      });
      this.setState({ error });
    } else {
      instance.detachEveryConnection();
      instance.deleteEveryEndpoint();
      this.setState({
        net,
        net_name,
        selectedLayer: null,
        nextLayerId: Object.keys(net).length,
        rebuildNet: true,
        selectedPhase: 0,
        error: [],
      });
    }

  }
  changeNetStatus(bool) {
    this.setState({ rebuildNet: bool });
  }
  changeNetPhase(phase) {
    const net = this.state.net;
    this.setState({ net: {}, selectedLayer: null });
    instance.detachEveryConnection();
    instance.deleteEveryEndpoint();
    this.setState({ net, selectedPhase: phase, rebuildNet: true });
  }
  dismissError(errorIndex) {
    const error = this.state.error;
    error.splice(errorIndex, 1);
    this.setState({ error });
  }
  addError(errorText) {
    const error = this.state.error;
    error.push(errorText);
    this.setState({ error });
  }
  dismissAllErrors() {
    this.setState({ error: [] });
  }
  copyTrain() {
    const net = this.state.net;
    Object.keys(net).forEach(layerId => {
      if (net[layerId].info.phase === 0) {
        net[layerId].info.phase = null;
      } else if (net[layerId].info.phase === 1) {
        this.deleteLayer(layerId);
      }
    });
    this.setState({
      net,
      selectedLayer: null,
      rebuildNet: true,
    });
  }
  trainOnly() {
    const net = this.state.net;
    const layer = net[this.state.selectedLayer];
    const layerId = this.state.selectedLayer;
    let index;
    if (layer.info.phase == null) {
      (layer.connection.output).forEach(outputId => {
        if (net[outputId].info.phase === 1) {
          index = layer.connection.output.indexOf(outputId);
          layer.connection.output.splice(index, 1);
          index = net[outputId].connection.input.indexOf(layerId);
          net[outputId].connection.input.splice(index, 1);
        }
      });
      (layer.connection.input).forEach(inputId => {
        if (net[inputId].info.phase === 1) {
          index = layer.connection.input.indexOf(inputId);
          layer.connection.input.splice(index, 1);
          index = net[inputId].connection.output.indexOf(layerId);
          net[inputId].connection.output.splice(index, 1);
        }
      });
    }
    layer.info.phase = 0;
    this.setState({ net });
  }
  render() {
    let loader = null;
    if (this.state.load) {
      loader = (<div className="loader"></div>);
    }
    return (
      <div className="container-fluid">
        <TopBar
          exportNet={this.exportNet}
          importNet={this.importNet}
        />
        <div className="content">
          <div className="pane">
            <ul className="nav nav-pills">
              <Pane />
              <li style={{paddingTop:'4px'}}>
                <button><span className="glyphicon glyphicon-cog" style={{fontSize:'24px'}}></span></button>
              </li>
              <Tabs selectedPhase={this.state.selectedPhase} changeNetPhase={this.changeNetPhase} />
            </ul>
          </div>
          {loader}
          <Canvas
            net={this.state.net}
            selectedPhase={this.state.selectedPhase}
            rebuildNet={this.state.rebuildNet}
            addNewLayer={this.addNewLayer}
            nextLayerId={this.state.nextLayerId}
            changeSelectedLayer={this.changeSelectedLayer}
            modifyLayer={this.modifyLayer}
            changeNetStatus={this.changeNetStatus}
            error={this.state.error}
            dismissError={this.dismissError}
            addError={this.addError}
          />
          <SetParams
            net={this.state.net}
            selectedLayer={this.state.selectedLayer}
            modifyLayer={this.modifyLayerParams}
            deleteLayer={this.deleteLayer}
            selectedPhase={this.state.selectedPhase}
            copyTrain={this.copyTrain}
            trainOnly={this.trainOnly}
          />
        </div>
      </div>
    );
  }
}

export default Content;
