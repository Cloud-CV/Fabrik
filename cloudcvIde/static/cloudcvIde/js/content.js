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
    this.deleteLayer = this.deleteLayer.bind(this);
    this.exportNet = this.exportNet.bind(this);
    this.importNet = this.importNet.bind(this);
    this.changeNetStatus = this.changeNetStatus.bind(this);
    this.changeNetPhase = this.changeNetPhase.bind(this);
    this.dismissError = this.dismissError.bind(this);
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
          // only for demo purpose - will be removed later
          document.getElementById('prototxt').innerHTML = response.result;
          prototxtId = response.id;
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
          top: `${30 + 100 * Math.floor(id / 4)}px`,
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
  dismissError(i){
    //const error = this.state.error;
    //error.splice(index, 1);

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
