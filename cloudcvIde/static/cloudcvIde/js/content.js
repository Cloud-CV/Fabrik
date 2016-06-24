import React from 'react';
import Canvas from './canvas';
import Pane from './pane';
import SetParams from './setParams';
import TopBar from './topBar';
import Tabs from './tabs';
import data from './data';

class Content extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      net: {},
      selectedLayer: null,
      nextLayerId: 0,
      rebuildNet: false,
      selectedPhase: 0,
      error:[],
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
    this.copyTrain = this.copyTrain.bind(this);
    this.addError = this.addError.bind(this);
    this.copyLayerToTest = this.copyLayerToTest.bind(this);
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
  modifyLayerParams(l,id = this.state.selectedLayer){
    const net = this.state.net;
    const layer = net[id];
    let index;
    const l1 = JSON.parse(JSON.stringify(layer))
    console.log('old layer');
    console.log(layer);
    console.log('new layer');
    console.log(l);

    if(this.state.selectedPhase === 1 && layer.info.phase === null){
      l.info.phase = 1;
      (l.connection.output).forEach(outputId => {
        if(net[outputId].info.phase === 0){
          index = l.connection.output.indexOf(outputId);
          l.connection.output.splice(index,1)
          index = net[outputId].connection.input.indexOf(id);
          net[outputId].connection.input.splice(index,1)
        }
      });
      (l.connection.input).forEach(inputId => {
        if(net[inputId].info.phase === 0){
          index = l.connection.input.indexOf(inputId);
          l.connection.input.splice(index,1)
          index = net[inputId].connection.output.indexOf(id);
          net[inputId].connection.output.splice(index,1)
        }
      });
      net[id] = l;
      this.setState({ net });
      console.log('added test layer');
      console.log(net);

      l1.info.phase = 0;
      l1.props.name.value = `${data[l1.info.type].name}${this.state.nextLayerId}`;
      (l1.connection.output).forEach(outputId => {
        if(net[outputId].info.phase === 1){
          index = l1.connection.output.indexOf(outputId);
          l1.connection.output.splice(index,1)
          index = net[outputId].connection.input.indexOf(id);
          net[outputId].connection.input.splice(index,1)
        }
      });
      (l1.connection.input).forEach(inputId => {
        if(net[inputId].info.phase === 1){
          index = l1.connection.input.indexOf(inputId);
          l1.connection.input.splice(index,1)
          index = net[inputId].connection.output.indexOf(id);
          net[inputId].connection.output.splice(index,1)
        }
      });

      const nextLayerId = 'l'+this.state.nextLayerId;

      (l1.connection.output).forEach(outputId => {
        net[outputId].connection.input.push(nextLayerId);
      });

      (l1.connection.input).forEach(inputId => {
        net[inputId].connection.output.push(nextLayerId);
      });

      this.addNewLayer(l1);
      console.log('added test layer');
      console.log(net);
    } else{
      net[id] = l;
      this.setState({ net });
    }

  }
  deleteLayer(id) {
    const net = this.state.net;
    const input = net[id].connection.input;
    const output = net[id].connection.output;
    let index;
    delete net[id];
    input.forEach(inputId => {
      index = net[inputId].connection.output.indexOf(id);
      net[inputId].connection.output.splice(index, 1);
    });
    output.forEach(outputId =>{
      index = net[outputId].connection.input.indexOf(id);
      net[outputId].connection.input.splice(index,1);
    });
    this.setState({ net, selectedLayer: null });
  }
  exportNet() {
    this.setState({error:[]})
    const error = [];
    const net = this.state.net;

    Object.keys(net).forEach(i => {
      const layer = net[i];
      Object.keys(layer.params).forEach(i => {
        const param = layer.params[i];
        if (param.required === true && param.value == '') {
          error.push('Error: "'+param.name+'" required in "'+layer.props.name.value+'" Layer');
        }
      });
    });

    if(error.length){
      this.setState({error:error})
    } else {
      $.ajax({
        url: '/cloudcvide/export',
        dataType: 'json',
        type: 'POST',
        data: {
          net: JSON.stringify(this.state.net),
        },
        success(response) {
          prototxtId = response.id;

          var exportResult=document.getElementById("exportResult");
          exportResult.style.display="block";

          var downloadAnchor= document.getElementById("download")
          downloadAnchor.href = '/media/prototxt/'+prototxtId+'.prototxt';


          $('html, body').animate(
            { scrollTop: $('#exportResult').offset().top },
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


  }
  importNet() {
    const formData = new FormData();
    formData.append('file', $('#inputFile')[0].files[0]);
    $.ajax({
      url: '/cloudcvide/import',
      dataType: 'json',
      type: 'POST',
      data: formData,
      processData: false,  // tell jQuery not to process the data
      contentType: false,
      success: function (response) {
        this.initialiseImportedNet(response.net);
      }.bind(this),
      error() {
        // console.log('failure');
      },
    });
  }
  initialiseImportedNet(net) {
    // this line will unmount all the layers
    // so that the new imported layers will all be mounted again
    const error = [];
    this.setState({ net: {}, selectedLayer: null, nextLayerId: 0, selectedPhase: 0,error: [] });
    Object.keys(net).forEach(i => {
      const l = net[i];
      const type = l.info.type;
      const id = +i.substring(1);
      if(data.hasOwnProperty(type)) {
        l.params = JSON.parse(JSON.stringify(data[type].params));
        Object.keys(l.importedParams).forEach(j => {
          l.params[j].value = l.importedParams[j];
        });
        l.props = JSON.parse(JSON.stringify(data[type].props));
        // default name
        l.props.name.value = `${data[type].name}${id}`;
        l.state = {
          top: `${130 + 100 * Math.floor(id / 4)}px`,
          left: `${30 + 170 * (id % 4)}px`,
          class: '',
        };
      } else {
        error.push("Error: Currently we do not support prototxt with \""+type+"\" Layer.");
      }


    });

    if(error.length){
      this.setState({error:error})
    } else {
      instance.detachEveryConnection();
      instance.deleteEveryEndpoint();
      this.setState({ net,
        selectedLayer: null,
        nextLayerId: Object.keys(net).length,
        rebuildNet: true,
        selectedPhase: 0,
        error:[],
      });
    }

  }
  changeNetStatus(bool) {
    this.setState({ rebuildNet: bool });
  }
  changeNetPhase(i) {
    const net = this.state.net;
    this.setState({ net: {}, selectedLayer: null });
    instance.detachEveryConnection();
    instance.deleteEveryEndpoint();
    this.setState({ net, selectedPhase: i, rebuildNet: true });
  }
  dismissError(i) {
    const error = this.state.error;
    error.splice(i, 1);
    this.setState({error:error})
  }
  addError(i) {
    const error = this.state.error;
    error.push(i);
    this.setState({error:error})
  }
  copyTrain() {
    console.log("copy train !");
    const net = this.state.net;
    Object.keys(net).forEach(layerId => {
      if(net[layerId].info.phase==0){
        net[layerId].info.phase=null;
      }
      else if(net[layerId].info.phase==1){
        this.deleteLayer(layerId);
      }
    });
    this.setState({ net,
      selectedLayer: null,
      rebuildNet: true,
    });
  }
  copyLayerToTest(){
    const net = this.state.net;
    net[this.state.selectedLayer].info.phase = null;
    this.setState({net});
  }
  render() {
    return (
      <div className="container-fluid">
        <TopBar
          exportNet={this.exportNet}
          importNet={this.importNet}
        />
        <Tabs selectedPhase={this.state.selectedPhase} changeNetPhase={this.changeNetPhase} />
        <div className="content row">
          <Pane />
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
            copyLayerToTest={this.copyLayerToTest}
          />
        </div>
      </div>
    );
  }
}

export default Content;
