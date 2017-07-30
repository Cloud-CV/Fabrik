import React from 'react';
import Canvas from './canvas';
import Pane from './pane';
import Models from './models'
import SetParams from './setParams';
import Tooltip from './tooltip'
import TopBar from './topBar';
import Tabs from './tabs';
import data from './data';
import netLayout from './netLayout_vertical';

class Content extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      net: {},
      net_name: null,
      selectedLayer: null,
      hoveredLayer: null,
      nextLayerId: 0,
      rebuildNet: false,
      selectedPhase: 0,
      error: [],
      load: false
    };
    this.addNewLayer = this.addNewLayer.bind(this);
    this.changeSelectedLayer = this.changeSelectedLayer.bind(this);
    this.changeHoveredLayer = this.changeHoveredLayer.bind(this);
    this.modifyLayer = this.modifyLayer.bind(this);
    this.adjustParameters = this.adjustParameters.bind(this);
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
  changeHoveredLayer(layerId) {
    const net = this.state.net;
    if (this.state.hoveredLayer) {
      // remove css from previously selected layer
      net[this.state.hoveredLayer].info.class = '';
    }
    if (layerId) {
      // css when layer is selected
      net[layerId].info.class = 'hover';
    }
    this.setState({ net, hoveredLayer: layerId });
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
        layer.params[param] = layer.params[param][0];
        const paramData = data[layer.info.type].params[param];
        if (layer.info.type == 'Python' && param == 'endPoint'){
          return;
        }
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

      const url = {'caffe': '/caffe/export', 'keras': '/keras/export', 'tensorflow': '/tensorflow/export', 'url': '/caffe/export'}
      this.setState({ load: true });
      $.ajax({
        url: url[framework],
        dataType: 'json',
        type: 'POST',
        data: {
          net: JSON.stringify(netData),
          net_name: this.state.net_name
        },
        success : function (response) {

          if (response.result == 'success' && framework == 'url'){
            var id = response.url.split('/')[2];
            id = id.split('.')[0];
            prompt('Your prototxt ID is ',id);
          }
          else if (response.result == 'success') {
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
          this.setState({ load: false });
        }
      });
    }
  }
  importNet(framework, id) {
    this.dismissAllErrors();
    const url = {'caffe': '/caffe/import', 'keras': '/keras/import', 'tensorflow': '/tensorflow/import', 'url': '/caffe/import'};
    const formData = new FormData();
    const caffe_fillers = ['constant', 'gaussian', 'positive_unitball', 'uniform', 'xavier', 'msra', 'bilinear'];
    const keras_fillers = ['Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 
    'VarianceScaling', 'Orthogonal', 'Identity', 'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'];
    if (framework == 'samplecaffe'){
      framework = 'caffe'
      formData.append('sample_id', id);
    }
    else if (framework == 'samplekeras'){
      framework = 'keras'
      formData.append('sample_id', id);
    }
    else if (framework == 'url'){
      const id = prompt('Please enter prototxt id ',id);
      formData.append('proto_id', id);
    }
    else
      formData.append('file', $('#inputFile'+framework)[0].files[0]);
    this.setState({ load: true });
    if (framework == 'keras'){
      var fillers = keras_fillers;
    }
    else{
      fillers = caffe_fillers;
    }
    data['Convolution']['params']['weight_filler']['options'] = fillers;
    data['Convolution']['params']['bias_filler']['options'] = fillers;
    data['Deconvolution']['params']['weight_filler']['options'] = fillers;
    data['Deconvolution']['params']['bias_filler']['options'] = fillers;
    data['Recurrent']['params']['weight_filler']['options'] = fillers;
    data['Recurrent']['params']['bias_filler']['options'] = fillers;
    data['RNN']['params']['weight_filler']['options'] = fillers;
    data['RNN']['params']['bias_filler']['options'] = fillers;
    data['LSTM']['params']['weight_filler']['options'] = fillers;
    data['LSTM']['params']['bias_filler']['options'] = fillers;
    data['InnerProduct']['params']['weight_filler']['options'] = fillers;
    data['InnerProduct']['params']['bias_filler']['options'] = fillers;
    data['Embed']['params']['weight_filler']['options'] = fillers;
    data['Bias']['params']['filler']['options'] = fillers;
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
      }
    });
  }
  initialiseImportedNet(net,net_name) {
    // this line will unmount all the layers
    // so that the new imported layers will all be mounted again
    const tempError = {};
    const error = [];
    const height = 0.05*window.innerHeight;
    const width = 0.45*window.innerWidth;
    // Initialize Python layer parameters to be empty
    data['Python']['params'] = {}
    this.setState({ net: {}, selectedLayer: null, hoveredLayer: null, nextLayerId: 0, selectedPhase: 0, error: [] });
    Object.keys(net).forEach(layerId => {
      var layer = net[layerId];
      const type = layer.info.type;
      // const index = +layerId.substring(1);
      if (data.hasOwnProperty(type)) {
        // add the missing params with default values
        Object.keys(data[type].params).forEach(param => {
          if (!layer.params.hasOwnProperty(param)) {
            // The initial value is a list with the first element being the actual value, and the second being a flag which 
            // controls wheter the parameter is disabled or not on the frontend.
            layer.params[param] = [data[type].params[param].value, false];
          }
          else {
            layer.params[param] = [layer.params[param], false];
          }
        });
        if (type == 'Convolution' || type == 'Pooling' || type == 'Upsample' || type == 'LocallyConnected' || type == 'Eltwise'){
          layer = this.adjustParameters(layer, 'layer_type', layer.params['layer_type'][0]);
        }
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
    // Layers which are not used alone
    let combined_layers = ['ReLU', 'LRN', 'BatchNorm', 'Dropout', 'Scale'];
    Object.keys(positions).forEach(layerId => {
      const layer = net[layerId];
      // Checking if the layer is one of the combined ones
      // and deciding vertical spacing accordingly
      if ($.inArray(layer.info.type, combined_layers) != -1){
        var y_space = 0;
      }
      else {
        y_space = 40;
      }
      var prev_top = 0;

      // Finding the position of the last(deepest) connected layer
      if (net[layer.connection.input[0]] != undefined){
        prev_top = 0;
        for (var i=0; i<layer.connection.input.length; i++){
          var temp = net[layer.connection.input[i]].state.top;
          temp = parseInt(temp.substring(0,temp.length-2));
          if (temp > prev_top){
            prev_top = temp;
          }
        }
      }
      // Graph does not centre properly on higher resolution screens
      layer.state = {
          top: `${height + prev_top + y_space + Math.ceil(41-height)}px`,
          left: `${width + 80 * positions[layerId][0]}px`,
          class: ''
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
        hoveredLayer: null,
        nextLayerId: Object.keys(net).length,
        rebuildNet: true,
        selectedPhase: 0,
        error: []
      });
    }
  }
  adjustParameters(layer, para, value) {
    if (para == 'layer_type'){
      if (layer.info['type'] == 'Convolution' || layer.info['type'] == 'Pooling'){
        if (value == '1D'){
          layer.params['caffe'] = [false, false];
          layer.params['kernel_h'] = [layer.params['kernel_h'][0], true];
          layer.params['kernel_d'] = [layer.params['kernel_d'][0], true];
          layer.params['pad_h'] = [layer.params['pad_h'][0], true];
          layer.params['pad_d'] = [layer.params['pad_d'][0], true];
          layer.params['stride_h'] = [layer.params['stride_h'][0], true];
          layer.params['stride_d'] = [layer.params['stride_d'][0], true];
          if (layer.info['type'] == 'Convolution'){
            layer.params['dilation_h'] = [layer.params['dilation_h'][0], true];
            layer.params['dilation_d'] = [layer.params['dilation_d'][0], true];
          }
        }
        else if (value == '2D'){
          layer.params['caffe'] = [true, false];
          layer.params['kernel_h'] = [layer.params['kernel_h'][0], false];
          layer.params['kernel_d'] = [layer.params['kernel_d'][0], true];
          layer.params['pad_h'] = [layer.params['pad_h'][0], false];
          layer.params['pad_d'] = [layer.params['pad_d'][0], true];
          layer.params['stride_h'] = [layer.params['stride_h'][0], false];
          layer.params['stride_d'] = [layer.params['stride_d'][0], true];
          if (layer.info['type'] == 'Convolution'){
            layer.params['dilation_h'] = [layer.params['dilation_h'][0], false];
            layer.params['dilation_d'] = [layer.params['dilation_d'][0], true];
          }
        }
        else {
          layer.params['caffe'] = [false, false];
          layer.params['kernel_h'] = [layer.params['kernel_h'][0], false];
          layer.params['kernel_d'] = [layer.params['kernel_d'][0], false];
          layer.params['pad_h'] = [layer.params['pad_h'][0], false];
          layer.params['pad_d'] = [layer.params['pad_d'][0], false];
          layer.params['stride_h'] = [layer.params['stride_h'][0], false];
          layer.params['stride_d'] = [layer.params['stride_d'][0], false];
          if (layer.info['type'] == 'Convolution'){
            layer.params['dilation_h'] = [layer.params['dilation_h'][0], false];
            layer.params['dilation_d'] = [layer.params['dilation_d'][0], false];
          }
        }
      }
      else if (layer.info['type'] == 'Upsample'){
        if (value == '1D'){
          layer.params['size_h'] = [layer.params['size_h'][0], true];
          layer.params['size_d'] = [layer.params['size_d'][0], true];
        }
        else if (value == '2D'){
          layer.params['size_h'] = [layer.params['size_h'][0], false];
          layer.params['size_d'] = [layer.params['size_d'][0], true];
        }
        else{
          layer.params['size_h'] = [layer.params['size_h'][0], false];
          layer.params['size_d'] = [layer.params['size_d'][0], false];
        }
      }
      else if (layer.info['type'] == 'LocallyConnected'){
        if (value == '1D'){
          layer.params['kernel_h'] = [layer.params['kernel_h'][0], true];
          layer.params['stride_h'] = [layer.params['stride_h'][0], true];
        }
      }
      else if (layer.info['type'] == 'Eltwise'){
        if (value == 'Average' || value == 'Dot'){
          layer.params['caffe'] = [false, false];
        }
      }
    }
    return layer;
  }
  changeNetStatus(bool) {
    this.setState({ rebuildNet: bool });
  }
  changeNetPhase(phase) {
    const net = this.state.net;
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
      rebuildNet: true
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
              {/* <li style={{paddingTop:'4px'}}>
                <button><span className="glyphicon glyphicon-cog" style={{fontSize:'24px'}}></span></button>
              </li> --> */}
              <Tabs selectedPhase={this.state.selectedPhase} changeNetPhase={this.changeNetPhase} />
              <Models importNet={this.importNet}/>
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
            changeHoveredLayer={this.changeHoveredLayer}
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
            adjustParameters={this.adjustParameters}
            deleteLayer={this.deleteLayer}
            selectedPhase={this.state.selectedPhase}
            copyTrain={this.copyTrain}
            trainOnly={this.trainOnly}
          />
          <Tooltip
            id={'tooltip_text'}
            net={this.state.net}
            hoveredLayer={this.state.hoveredLayer}
          />
        </div>
      </div>
    );
  }
}

export default Content;

