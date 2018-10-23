import React from 'react';
import Field from './field';
import data from './data';

class SetParams extends React.Component {
  constructor(props) {
    super(props);
    this.changeParams = this.changeParams.bind(this);
    this.changeProps = this.changeProps.bind(this);
    this.trainOnly = this.trainOnly.bind(this);
    this.close = this.close.bind(this);
    this.handleKeyPress = this.handleKeyPress.bind(this);
  }
  changeProps(prop, value) {
    const net = this.props.net;
    let layer = net[this.props.selectedLayer];
    layer = JSON.parse(JSON.stringify(layer));
    layer.props[prop] = value;
    this.props.performSharedUpdate(this.props.selectedLayer, prop, value, true);
    this.props.modifyLayer(layer);
  }
  changeParams(para, value) {
    const net = this.props.net;
    let layer = net[this.props.selectedLayer];
    layer = JSON.parse(JSON.stringify(layer));
    var intParams = ["crop_size", "num_output", "new_height", "new_width", "height", "width", "kernel_h", "kernel_w",
                     "kernel_d", "stride_h", "stride_w", "stride_d", "pad_h", "pad_w", "pad_d", "size_h", "size_w",
                     "size_d", "n"];
    if (intParams.includes(para)){
      value = parseInt(value);
      if(isNaN(value))
        value = 0;
    }
    layer.params[para] = [value, false];
    this.props.performSharedUpdate(this.props.selectedLayer, para, value, false);
    this.props.modifyLayer(this.props.adjustParameters(layer, para, value));
  }
  close() {
    this.props.updateLayerWithShape(this.props.net[this.props.selectedLayer], this.props.selectedLayer);
    this.props.changeSelectedLayer(null);
  }
  trainOnly(e) {
    if (e.target.checked) {
      this.props.trainOnly();
    }
  }
  handleKeyPress(event){
     if (event.key == 'Delete'){
      this.props.deleteLayer(this.props.selectedLayer);
    }
  }
  componentDidMount(){
    document.addEventListener("keydown", this.handleKeyPress, false);
  }
  componentWillUnmount(){
    document.removeEventListener("keydown", this.handleKeyPress, false);
  }
  render() {
    if (this.props.selectedLayer) {
      const params = [];
      const props = [];
      const layer = this.props.net[this.props.selectedLayer];

      let trainOnlyCheckBox = null;
      if (this.props.selectedPhase === 0) {
        trainOnlyCheckBox = (
          <div style={{display: "flex"}}>
            <label className="sidebar-heading" style={{fontSize:"0.85em"}}>
              TRAIN ONLY
            </label>
            <div className="paramsCheckbox">
              <input
                type="checkbox"
                onChange={this.trainOnly}
                id="trainOnlyCheckBox"
              />
              <label htmlFor={"trainOnlyCheckBox"}></label>
            </div>
          </div>
        );
      }

      Object.keys(data[layer.info.type].params).forEach(param => {
        if (param != 'caffe'){
          params.push(
            <Field
              id={param}
              key={param}
              data={data[layer.info.type].params[param]}
              value={layer.params[param][0]}
              disabled={((layer.info.phase === null) && (this.props.selectedPhase === 1) && (data[layer.info.type].learn)) ||
                (layer.params[param][1])}
              changeField={this.changeParams}
            />
          );
        }
      });

      Object.keys(data[layer.info.type].props).forEach(prop => {
        props.push(
          <Field
            id={prop}
            key={prop}
            data={data[layer.info.type].props[prop]}
            value={layer.props[prop]}
            disabled={(layer.info.phase === null) && (this.props.selectedPhase === 1) && (data[layer.info.type].learn)}
            changeField={this.changeProps}
          />
        );
      });


      return (
        <div className="setparams setparamsActive" >
          <div className="setHead">
            <h5 className="sidebar-heading">LAYER SELECTED</h5>
            <h4>{layer.props.name}</h4>
            <span className="glyphicon glyphicon-remove-sign closeSign" onClick={() => this.close()} aria-hidden="true"></span>
          </div>
          <div className="setContain">
            <form className="form-horizontal">
              {props}
            </form>
            <form className="form-horizontal">
              {params}
            </form>
            <br/>
            {trainOnlyCheckBox}
            <br/>
            <button
              type="button"
              className="btn btn-block deleteLayerButton sidebar-heading"
              disabled={(layer.info.phase === null) && (this.props.selectedPhase === 1) && (data[layer.info.type].learn)}
              onClick={() => this.props.deleteLayer(this.props.selectedLayer)}
            >
              DELETE LAYER
            </button>
          </div>
        </div>
      );
    } else {
      let copyTrainButton = null;
      if (this.props.selectedPhase === 1) {
        copyTrainButton = (
          <button
            className="btn btn-primary"
            onClick={this.props.copyTrain}
            style={{ marginLeft: '80px' }}
          >
            Copy train net
          </button>
        );
      }

      return (
        <div className="col-md-3 setparams" >
          <div className="setHead" style={{ color: 'white' }}>
            Settings
          </div>
          <div style={{ padding: '30px' }}>
            select a layer to set its parameters
          </div>
          {copyTrainButton}
        </div>
    );
    }
  }
}

SetParams.propTypes = {
  selectedLayer: React.PropTypes.string,
  net: React.PropTypes.object,
  deleteLayer: React.PropTypes.func,
  modifyLayer: React.PropTypes.func,
  adjustParameters: React.PropTypes.func,
  trainOnly: React.PropTypes.func,
  selectedPhase: React.PropTypes.number,
  copyTrain: React.PropTypes.func,
  changeSelectedLayer: React.PropTypes.func,
  updateLayerWithShape: React.PropTypes.func,
  performSharedUpdate: React.PropTypes.func
};

export default SetParams;
