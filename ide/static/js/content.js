import React from 'react';
import Canvas from './canvas';
import Pane from './pane';
import SetParams from './setParams';
import Tooltip from './tooltip'
import TopBar from './topBar';
import Tabs from './tabs';
import data from './data';
import netLayout from './netLayout_vertical';
import Modal from 'react-modal';
import ModelZoo from './modelZoo';
import Login from './login';
import ImportTextbox from './importTextbox';
import UrlImportModal from './urlImportModal';
import $ from 'jquery'

const infoStyle = {
  content : {
    top                   : '50%',
    left                  : '50%',
    right                 : '60%',
    bottom                : 'auto',
    marginRight           : '-50%',
    transform             : 'translate(-50%, -50%)',
    borderRadius          : '8px'
  },
  overlay: {
    zIndex                : 100
  }
};

class Content extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      net: {},
      net_name: 'Untitled',
      draggingLayer: null,
      selectedLayer: null,
      hoveredLayer: null,
      nextLayerId: 0,
      rebuildNet: false,
      selectedPhase: 0,
      error: [],
      info: [],
      load: false,
      modalIsOpen: false,
      totalParameters: 0,
      modelConfig: null,
      modelFramework: 'caffe',
      user_id: null
    };
    this.addNewLayer = this.addNewLayer.bind(this);
    this.changeSelectedLayer = this.changeSelectedLayer.bind(this);
    this.changeHoveredLayer = this.changeHoveredLayer.bind(this);
    this.componentWillMount = this.componentWillMount.bind(this);
    this.modifyLayer = this.modifyLayer.bind(this);
    this.setDraggingLayer = this.setDraggingLayer.bind(this);
    this.changeNetName = this.changeNetName.bind(this);
    this.adjustParameters = this.adjustParameters.bind(this);
    this.modifyLayerParams = this.modifyLayerParams.bind(this);
    this.deleteLayer = this.deleteLayer.bind(this);
    this.exportPrep = this.exportPrep.bind(this);
    this.exportNet = this.exportNet.bind(this);
    this.importNet = this.importNet.bind(this);
    this.changeNetStatus = this.changeNetStatus.bind(this);
    this.changeNetPhase = this.changeNetPhase.bind(this);
    this.dismissError = this.dismissError.bind(this);
    this.addError = this.addError.bind(this);
    this.dismissAllErrors = this.dismissAllErrors.bind(this);
    this.addInfo = this.addInfo.bind(this);
    this.dismissInfo = this.dismissInfo.bind(this);
    this.copyTrain = this.copyTrain.bind(this);
    this.trainOnly = this.trainOnly.bind(this);
    this.openModal = this.openModal.bind(this);
    this.closeModal = this.closeModal.bind(this);
    this.saveDb = this.saveDb.bind(this);
    this.loadDb = this.loadDb.bind(this);
    this.infoModal = this.infoModal.bind(this);
    this.toggleSidebar = this.toggleSidebar.bind(this);
    this.zooModal = this.zooModal.bind(this);
    this.textboxModal = this.textboxModal.bind(this);
    this.urlModal = this.urlModal.bind(this);
    this.setModelConfig = this.setModelConfig.bind(this);
    this.setModelFramework = this.setModelFramework.bind(this);
    this.setModelUrl = this.setModelUrl.bind(this);
    this.setModelFrameworkUrl = this.setModelFrameworkUrl.bind(this);
    this.loadLayerShapes = this.loadLayerShapes.bind(this);
    this.calculateParameters = this.calculateParameters.bind(this);
    this.getLayerParameters = this.getLayerParameters.bind(this);
    this.updateLayerShape = this.updateLayerShape.bind(this);
    this.setUserId = this.setUserId.bind(this);
    this.modalContent = null;
    this.modalHeader = null;
    // Might need to improve the logic of clickEvent
    this.clickEvent = false;
    this.handleClick = this.handleClick.bind(this);
  }
  openModal() {
    this.setState({ modalIsOpen: true });
  }
  closeModal() {
    this.setState({ modalIsOpen: false });
  }
  setUserId(user_id) {
    this.setState({ user_id: user_id });
  }
  addNewLayer(layer) {
    const net = this.state.net;
    const layerId = `l${this.state.nextLayerId}`;
    var totalParameters = this.state.totalParameters;
    net[layerId] = layer;
    // Parsing for integer parameters when new layers are added as by default all params are string
    // In case some parameters are missed please cover them too
    var intParams = ["crop_size", "num_output", "new_height", "new_width", "height", "width", "kernel_h", "kernel_w",
                      "kernel_d", "stride_h", "stride_w", "stride_d", "pad_h", "pad_w", "pad_d", "size_h", "size_w",
                      "size_d", "n"];
    Object.keys(net[layerId].params).forEach(param => {
      if (intParams.includes(param)){
        net[layerId].params[param][0] = parseInt(net[layerId].params[param][0]);
        if (isNaN(net[layerId].params[param][0]))
          net[layerId].params[param][0] = 0;
      }
    });
    this.updateLayerShape(net, layerId);
    // Check for only layers with valid shape
    if (net[layerId]['shape']['input'] != null && net[layerId]['shape']['output'] != null) {
      net[layerId]['info']['parameters'] = this.getLayerParameters(net[layerId], net);
      totalParameters += net[layerId]['info']['parameters'];
    }
    this.setState({ net, nextLayerId: this.state.nextLayerId + 1, totalParameters: totalParameters });
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
    if (this.state.hoveredLayer && this.state.hoveredLayer in net) {
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
    var oldLayerParams = this.state.totalParameters;
    if (net[layerId]['shape']['input'] != null && net[layerId]['shape']['output'] != null)
      oldLayerParams -= net[layerId]['info']['parameters'];
    net[layerId] = layer;
    this.updateLayerShape(net, layerId);
    if (net[layerId]['shape']['input']!=null && net[layerId]['shape']['output']!=null) {
      net[layerId]['info']['parameters'] = this.getLayerParameters(net[layerId], net);
      oldLayerParams += net[layerId]['info']['parameters'];
    }
    this.setState({ net: net, totalParameters: oldLayerParams });
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
    const layerIdNum = parseInt(layerId.substring(1,layerId.length)); //numeric value of the layerId
    const nextLayerId = this.state.nextLayerId - 1 == layerIdNum ? layerIdNum : this.state.nextLayerId;
       //if last layer was deleted nextLayerId is replaced by deleted layer's id
    var totalParameters = this.state.totalParameters;
    let index;
    totalParameters -= this.getLayerParameters(net[layerId], net);
    delete net[layerId];
    input.forEach(inputId => {
      index = net[inputId].connection.output.indexOf(layerId);
      net[inputId].connection.output.splice(index, 1);
    });
    output.forEach(outputId => {
      index = net[outputId].connection.input.indexOf(layerId);
      net[outputId].connection.input.splice(index, 1);
    });
    this.setState({ net, selectedLayer: null, nextLayerId: nextLayerId, totalParameters: totalParameters });
  }

  updateLayerShape(net, layerId) {
    const netData = JSON.parse(JSON.stringify(net));
    Object.keys(netData[layerId].params).forEach(param => {
      netData[layerId].params[param] = netData[layerId].params[param][0];
    });
    net[layerId]['shape'] = {};
    net[layerId]['shape']['input'] = null;
    net[layerId]['shape']['output'] = null;
    net[layerId]['info']['parameters'] = 0;

    $.ajax({
      url: 'layer_parameter/',
      dataType: 'json',
      type: 'POST',
      async: false,
      data: {
        net: JSON.stringify(netData),
        layerId: layerId
      },
      success : function (response) {
        if (response.result == "success") {
          if (response.net[layerId]['shape']['input'] != null)
            net[layerId]['shape']['input'] = response.net[layerId]['shape']['input'].slice();
          if (response.net[layerId]['shape']['output'] != null)
            net[layerId]['shape']['output'] = response.net[layerId]['shape']['output'].slice();
        }
        else
          this.addError(response.error);
      }.bind(this)
    });
  }
  getLayerParameters(layer, net) {
    // check for layers with no shape to avoid errors
    // this can be improved further.
    if (layer['shape']['input'] == null || layer['shape']['output'] == null) {
      return 0;
    }
    // obtain the total parameters of the model
    var weight_params = 0;
    var bias_params = 0;

    var filter_layers = ["Convolution", "Deconvolution"];
    var fc_layers = ["InnerProduct", "Embed", "Recurrent", "LSTM"];

    if(filter_layers.includes(layer.info.type)) {
      // if layer is Conv or DeConv calculating total parameter of the layer using:
      // N_Input * K_H * K_W * N_Output
      var kernel_params = 1;
      if('kernel_h' in layer.params && layer.params['kernel_h'][0] != '')
        kernel_params *= layer.params['kernel_h'][0];
      if('kernel_w' in layer.params && layer.params['kernel_w'][0] != '')
        kernel_params *= layer.params['kernel_w'][0];
      if('kernel_d' in layer.params && layer.params['kernel_d'][0] != '')
        kernel_params *= layer.params['kernel_d'][0];

      weight_params = layer.shape['input'][0] * kernel_params * layer.params['num_output'][0];
      bias_params += layer.params['num_output'][0];
    }
    else if(fc_layers.includes(layer.info.type)) {
      // if layer is one of Recurrent layer or Fully Connected layers calculate parameters using:
      // Num_Input * Num_Ouput
      // if previous layer is D-dimensional then obtain the total inputs by (N1xN2x...xNd)
      var inputParams = 1;
      for(var i=0;i<layer.shape['input'].length;i++) {
        if(layer.shape['input'][i] != 0)
          inputParams *= layer.shape['input'][i];
      }
      weight_params = inputParams * layer.params['num_output'][0];
      bias_params = layer.params['num_output'][0];
    }
    if(layer.info.type == "BatchNorm") {
      let cnt = 2;
      if(layer.connection['output'].length > 0) {
        const childLayer = net[layer.connection['output'][0]];
        if(childLayer.info.type == "Scale") {
          if(childLayer.params['scale'][0] == true)
            cnt +=1
          if(childLayer.params['bias_term'][0] == true)
            cnt +=1;
        }
      }
      weight_params = cnt * layer.shape['output'][0];
    }
    if('use_bias' in layer.params) {
      if (layer.params['use_bias'][0] == false)
        bias_params = 0;
    }

    // Update the total parameters of model after considering this layer.
    return (weight_params + bias_params);
  }
  calculateParameters(net) {
    // Iterate over model's each layer & separately add the contribution of each layer
    var totalParameters = 0;
    Object.keys(net).sort().forEach(layerId => {
      const layer = net[layerId];
      net[layerId]['info']['parameters'] = this.getLayerParameters(layer, net);
      totalParameters += net[layerId]['info']['parameters'];
    });
    this.setState({ net: net, totalParameters: totalParameters});
  }
  loadLayerShapes() {
    this.dismissAllErrors();
    // Making call to endpoint inorder to obtain shape of each layer i.e. input & output shape
    const netData = JSON.parse(JSON.stringify(this.state.net));
    $.ajax({
      url: 'model_parameter/',
      dataType: 'json',
      type: 'POST',
      data: {
        net: JSON.stringify(netData)
      },
      success : function (response) {
        const net = response.net;
        // call to intermediate method which will iterate over layers & calculate the parameters separately
        this.calculateParameters(net);
        // update the net object with shape attributes added
        this.setState({ net });
      }.bind(this),
      error() {
        //console.log('error'+response.error);
      }
    });
  }
  exportPrep(callback) {
    this.dismissAllErrors();
    const error = [];
    const netObj = JSON.parse(JSON.stringify(this.state.net));
    if (Object.keys(netObj).length == 0) {
      this.addError("No model available for export");
      return;
    }

    Object.keys(netObj).forEach(layerId => {
      const layer = netObj[layerId];
      Object.keys(layer.params).forEach(param => {
        layer.params[param] = layer.params[param][0];
        const paramData = data[layer.info.type].params[param];
        if (layer.info.type == 'Python' || param == 'endPoint'){
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
      callback(netObj);
    }
  }
  exportNet(framework) {
    this.exportPrep(function(netData) {
      Object.keys(netData).forEach(layerId => {
        delete netData[layerId].state;
      });

      const url = {'caffe': '/caffe/export', 'keras': '/keras/export', 'tensorflow': '/tensorflow/export'}
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

          if (response.result == 'success') {
            const downloadAnchor = document.getElementById('download');
            downloadAnchor.download = response.name;
            downloadAnchor.href = response.url;
            downloadAnchor.click();
            if ('customLayers' in response && response.customLayers.length !== 0) {
              this.addInfo(
                <span>
                  <span>This network uses custom layers, to download click on: </span>
                  {response.customLayers.map((layer, index) => {
                    return (
                      <span key={index}>
                        <a onClick={function() {
                          downloadAnchor.download = layer.filename;
                          downloadAnchor.href = layer.url;
                          downloadAnchor.click();
                        }} style={{fontWeight: 'bold'}}>
                          {layer.name}
                        </a>
                        {index != response.customLayers.length-1 && <span>, </span>}
                      </span>
                    );
                  })}
                </span>
              );
            }
          } else if (response.result == 'error') {
            this.addError(response.error);
          }
          this.setState({ load: false });
        }.bind(this),
        error : function () {
          this.setState({ load: false });
          this.addError("Error");
        }.bind(this)
      });
    }.bind(this));
  }
  importNet(framework, id) {
    this.dismissAllErrors();
    this.closeModal();
    this.clickEvent = false;
    const url = {'caffe': '/caffe/import', 'keras': '/keras/import', 'tensorflow': '/tensorflow/import'};
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
    else if (framework == 'input') {
      framework = this.state.modelFramework;
      formData.append('config', this.state.modelConfig);
    }
    else if (framework == 'url') {
      framework = this.state.modelFramework;
      formData.append('url', this.state.modelUrl);
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
          if (Object.keys(this.state.net).length)
            this.loadLayerShapes();
        } else if (response.result === 'error'){
          this.addError(response.error);
        }
        this.setState({ load: false });
      }.bind(this),
      error : function () {
        this.setState({ load: false });
        this.addError("Error");
      }.bind(this)
    });
  }
  initialiseImportedNet(net,net_name) {
    // this line will unmount all the layers
    // so that the new imported layers will all be mounted again
    const tempError = {};
    // Initialize Python layer parameters to be empty
    data['Python']['params'] = {}
    this.setState({ net: {}, selectedLayer: null, hoveredLayer: null, nextLayerId: 0, selectedPhase: 0, error: [] });
    Object.keys(net).forEach(layerId => {
      var layer = net[layerId];
      const type = layer.info.type;
      // extract unique input & output nodes
      net[layerId]['connection']['input'] = net[layerId]['connection']['input'].filter((val,id,array) => array.indexOf(val) == id);
      net[layerId]['connection']['output'] = net[layerId]['connection']['output'].filter((val,id,array) => array.indexOf(val) == id);
      // const index = +layerId.substring(1);
      if (type == 'Python'){
        Object.keys(layer.params).forEach(param => {
          layer.params[param] = [layer.params[param], false];
        });
        layer.params['caffe'] = [true, false];
      }
      if (data.hasOwnProperty(type)) {
        // add the missing params with default values
        Object.keys(data[type].params).forEach(param => {
          if (!layer.params.hasOwnProperty(param)) {
            // The initial value is a list with the first element being the actual value, and the second being a flag which
            // controls whether the parameter is disabled or not on the frontend.
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
    if (tempError.length == undefined) {
      netLayout(net);
    }

    if (Object.keys(tempError).length) {
      const errorLayers = Object.keys(tempError).join(', ');
      this.setState({ error: [`Error: Currently we do not support these layers: ${errorLayers}.`] });
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
        error: [],
        totalParameters: 0
      });
    }
  }
  setDraggingLayer(id) {
    this.setState({ draggingLayer: id })
  }
  changeNetName(event) {
    this.setState({net_name: event.target.value});
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
    this.setState({ error, info: []});
  }
  addError(errorText) {
    const error = this.state.error;
    error.push(errorText);
    this.setState({ error });
  }
  dismissAllErrors() {
    this.setState({ error: [] });
    this.setState({ info: [] });
  }
  addInfo(infoContent) {
    const info = this.state.info;
    info.push(infoContent)
    this.setState({ info, error: [] })
  }
  dismissInfo(infoIndex) {
    const info = this.state.info;
    info.splice(infoIndex, 1);
    this.setState({ info });
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
  saveDb(){
    this.exportPrep(function(netData) {
      Object.keys(netData).forEach(layerId => {
        delete netData[layerId].state;
      });
      this.setState({ load: true });
      $.ajax({
        url: '/caffe/save',
        dataType: 'json',
        type: 'POST',
        data: {
          net: JSON.stringify(netData),
          net_name: this.state.net_name
        },
        success : function (response) {
          if (response.result == 'success'){
            var url = 'http://fabrik.cloudcv.org/caffe/load?id='+response.id;
            this.modalHeader = 'Your model url is:';
            this.modalContent = (<a href={url}>{url}</a>);
            this.openModal();
          } else if (response.result == 'error') {
            this.addError(response.error);
          }
          this.setState({ load: false });
        }.bind(this),
        error() {
          this.setState({ load: false });
        }
      });
    }.bind(this));
  }
  componentWillMount(){
    var url = window.location.href;
    var urlParams = {};
    url = url.split('#')[0];
    url.replace(
    new RegExp("([^?=&]+)(=([^&]*))?", "g"),
    function($0, $1, $2, $3) {
      urlParams[$1] = $3;
      }
    );
    if ('id' in urlParams){
      this.loadDb(urlParams['id']);
    }
  }
  loadDb(id) {
    this.dismissAllErrors();
    const formData = new FormData();
    formData.append('proto_id', id);
    $.ajax({
      url: '/caffe/load',
      dataType: 'json',
      type: 'POST',
      data: formData,
      processData: false,  // tell jQuery not to process the data
      contentType: false,
      success: function (response) {
        if (response.result === 'success'){
          this.initialiseImportedNet(response.net,response.net_name);
          if (Object.keys(response.net).length){
            this.calculateParameters(response.net);
          }
        } else if (response.result === 'error'){
          this.addError(response.error);
        }
        this.setState({ load: false });
      }.bind(this),
      error() {
        this.setState({ load: false });
      }
    });
  }
  infoModal() {
    this.modalHeader = "About"
    this.modalContent = `Fabrik is an online collaborative platform to build and visualize deep\
                         learning models via a simple drag-and-drop interface. It allows researchers to\
                         collaboratively develop and debug models using a web GUI that supports importing,\
                         editing and exporting networks written in widely popular frameworks like Caffe,\
                         Keras, and TensorFlow.`;
    this.openModal();
  }
  toggleSidebar() {
    $('#sidebar').toggleClass('visible');
    $('.sidebar-button').toggleClass('close');
  }
  zooModal() {
    this.modalHeader = null;
    this.modalContent = <ModelZoo importNet={this.importNet} />;
    this.openModal();
  }
  setModelFramework(e) {
    const el = e.target;
    const modelFramework = el.dataset.framework;
    this.setState({modelFramework});
    $('.import-textbox-tab.selected').removeClass('selected');
    $(el).addClass('selected');
  }
  setModelFrameworkUrl(e) {
    const el = e.target;
    const modelFramework = el.dataset.framework;
    this.setState({modelFramework});
    $('.url-import-modal-tab.selected').removeClass('selected');
    $(el).addClass('selected');
  }
  setModelConfig(e) {
    const modelConfig = e.target.value;
    this.setState({modelConfig});
  }
  setModelUrl(url) {
    this.setState({ modelUrl: url});
  }
  textboxModal() {
    this.modalHeader = null;
    this.modalContent = <ImportTextbox
                          modelConfig={this.state.modelConfig}
                          modelFramework={this.state.modelFramework}
                          setModelConfig={this.setModelConfig}
                          setModelFramework={this.setModelFramework}
                          importNet={this.importNet}
                          addError={this.addError}
                        />;
    this.openModal();
  }
  urlModal() {
    this.modalHeader = null;
    this.modalContent = <UrlImportModal
                          modelFramework={this.state.modelFramework}
                          setModelFramework={this.setModelFrameworkUrl}
                          setModelUrl={this.setModelUrl}
                          importNet={this.importNet}
                          addError={this.addError}
                        />;
    this.openModal();
  }
  handleClick(event) {
    event.preventDefault();
    this.clickEvent = true;

    const net = this.state.net;
    // extracting layerId from Pane id which is in form LayerName_Button
    const id = event.target.id.split('_')[0];
    const prev = net[`l${this.state.nextLayerId-1}`];
    const next = data[id];
    const zoom = instance.getZoom();
    const layer = {};
    let phase = this.state.selectedPhase;

    if (this.state.nextLayerId>0 //makes sure that there are other layers
      && data[prev.info.type].endpoint.src == "Bottom" //makes sure that the source has a bottom
      && next.endpoint.trg == "Top") { //makes sure that the target has a top
        layer.connection = { input: [], output: [] };
        layer.info = {
          type: id.toString(),
          phase,
          class: ''
        }
        layer.params = {
          'endPoint' : [next['endpoint'], false] //This key is endpoint in data.js, but endPoint in everywhere else.
        }
        Object.keys(next.params).forEach(j => {
          layer.params[j] = [next.params[j].value, false]; //copys all params from data.js
        });
        layer.props = JSON.parse(JSON.stringify(next.props)) //copys all props rom data.js
        layer.state = {
          top: `${(parseInt(prev.state.top.split('px')[0])/zoom + 80)}px`, // This makes the new layer is exactly 80px under the previous one.
          left: `${(parseInt(prev.state.left.split('px')[0])/zoom)}px`, // This aligns the new layer with the previous one.
          class: ''
        }
        layer.props.name = `${next.name}${this.state.nextLayerId}`;
        prev.connection.output.push(`l${this.state.nextLayerId}`);
        layer.connection.input.push(`l${this.state.nextLayerId-1}`);
        this.addNewLayer(layer);
    }

    else if (Object.keys(net).length == 0) { // if there are no layers
      layer.connection = { input: [], output: [] };
      layer.info = {
            type: id.toString(),
            phase,
            class: ''
          }
      layer.params = {
        'endPoint' : [next['endpoint'], false] //This key is endpoint in data.js, but endPoint in everywhere else.
      }
      Object.keys(next.params).forEach(j => {
        layer.params[j] = [next.params[j].value, false];  //copys all params from data.js
      });
      layer.props = JSON.parse(JSON.stringify(next.props)) //copys all props from data.js
      const height = Math.round(0.05*window.innerHeight, 0); // 5% of screen height, rounded to zero decimals
      const width = Math.round(0.35*window.innerWidth, 0); // 35% of screen width, rounded to zero decimals
      var top = height + Math.ceil(81-height);
      var left = width;
      layer.state = {
            top: `${top}px`,
            left: `${left}px`,
            class: ''
          }
      layer.props.name = `${next.name}${this.state.nextLayerId}`;
      this.addNewLayer(layer);
    }
  }
  render() {
    let loader = null;
    if (this.state.load) {
      loader = (<div className="loaderOverlay">
                  <div className="loader"></div>
                </div>);
    }
    return (
        <div id="parent">
        <a className="sidebar-button" onClick={this.toggleSidebar}></a>
        <div id="sidebar">
          <div id="logo_back">
            <a href="http://fabrik.cloudcv.org"><img src={'/static/img/fabrik_t.png'} className="img-responsive" alt="logo" id="logo"/></a>
          </div>
          <div id="sidebar-scroll" className="col-md-12">
             <h5 className="sidebar-heading">ACTIONS</h5>
             <TopBar
              exportNet={this.exportNet}
              importNet={this.importNet}
              saveDb={this.saveDb}
              zooModal={this.zooModal}
              textboxModal={this.textboxModal}
              urlModal={this.urlModal}
             />
             <h5 className="sidebar-heading">LOGIN</h5>
             <Login setUserId={this.setUserId}></Login>
             <h5 className="sidebar-heading">INSERT LAYER</h5>
             <Pane
             handleClick = {this.handleClick}
             setDraggingLayer = {this.setDraggingLayer}
             />
             <div className="text-center">
              <Tabs selectedPhase={this.state.selectedPhase} changeNetPhase={this.changeNetPhase} />
             </div>
             <h5 className="sidebar-heading">EXTRAS</h5>
             <a className="btn btn-block extra-buttons text-left" onClick={this.infoModal}>About Us</a>
             <a className="btn btn-block extra-buttons text-left" href="https://github.com/Cloud-CV/Fabrik" target="_blank">GitHub</a>
             <a className="btn btn-block extra-buttons text-left" href="http://cloudcv.org" target="_blank">CloudCV</a>
          </div>
        </div>
      <div id="main">
          <input type="text"
            className={$.isEmptyObject(this.state.net) ? "hidden": ""}
            id="netName"
            placeholder="Net name"
            value={this.state.net_name}
            onChange={this.changeNetName}
            spellCheck="false"
          />
          {loader}
          <Canvas
            net={this.state.net}
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
            info={this.state.info}
            dismissInfo={this.dismissInfo}
            addInfo={this.addInfo}
            clickEvent={this.clickEvent}
            totalParameters={this.state.totalParameters}
            selectedPhase={this.state.selectedPhase}
            draggingLayer={this.state.draggingLayer}
            setDraggingLayer={this.setDraggingLayer}
            selectedLayer={this.state.selectedLayer}
          />
          <SetParams
            net={this.state.net}
            selectedLayer={this.state.selectedLayer}
            modifyLayer={this.modifyLayerParams}
            adjustParameters={this.adjustParameters}
            changeSelectedLayer={this.changeSelectedLayer}
            deleteLayer={this.deleteLayer}
            selectedPhase={this.state.selectedPhase}
            copyTrain={this.copyTrain}
            trainOnly={this.trainOnly}
            updateLayerWithShape={this.modifyLayer}
          />
          <Tooltip
            id={'tooltip_text'}
            net={this.state.net}
            hoveredLayer={this.state.hoveredLayer}
          />
          <Modal
            isOpen={this.state.modalIsOpen}
            onRequestClose={this.closeModal}
            style={infoStyle}
            contentLabel="Modal">
            <button type="button" style={{padding: 5+'px'}} className="close" onClick={this.closeModal}>&times;</button>
            <h4>{ this.modalHeader }</h4>
            { this.modalContent }
          </Modal>
        </div>
      </div>
    );
  }
}

export default Content;
