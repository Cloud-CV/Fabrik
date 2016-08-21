import React from 'react';
import Field from './field';
import data from './data';

class SetParams extends React.Component {
  constructor(props) {
    super(props);
    this.changeParams = this.changeParams.bind(this);
    this.changeProps = this.changeProps.bind(this);
    this.trainOnly = this.trainOnly.bind(this);
  }
  changeProps(prop, value) {
    const net = this.props.net;
    let layer = net[this.props.selectedLayer];
    layer = JSON.parse(JSON.stringify(layer));
    layer.props[prop] = value;
    this.props.modifyLayer(layer);
  }
  changeParams(para, value) {
    const net = this.props.net;
    let layer = net[this.props.selectedLayer];
    layer = JSON.parse(JSON.stringify(layer));
    layer.params[para] = value;
    this.props.modifyLayer(layer);
  }
  trainOnly(e) {
    if (e.target.checked) {
      this.props.trainOnly();
    }
  }
  render() {
    if (this.props.selectedLayer) {
      const params = [];
      const props = [];
      const layer = this.props.net[this.props.selectedLayer];

      let trainOnlyCheckBox = null;
      if (this.props.selectedPhase === 0) {
        trainOnlyCheckBox = (
          <div className="form-group" style={{ marginTop: '30px' }}>
            <label
              className="col-sm-6 control-label"
            >
              train only
            </label>
            <div className="col-sm-6">
              <input
                type="checkbox"
                onChange={this.trainOnly}
              />
            </div>
          </div>
        );
      }

      Object.keys(data[layer.info.type].params).forEach(param => {
        params.push(
          <Field
            id={param}
            key={param}
            data={data[layer.info.type].params[param]}
            value={layer.params[param]}
            disabled={(layer.info.phase === null) && (this.props.selectedPhase === 1) && (data[layer.info.type].learn)}
            changeField={this.changeParams}
          />
        );
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

          <div className="setHead" style={{ color: data[layer.info.type].color }}>
            {layer.props.name} layer selected
          </div>
          <div className="setContain">
            <form className="form-horizontal">
              Properties
              {props}
            </form>
            <br />
            <form className="form-horizontal">
              Parameters
              {params}
            </form>
            <button
              type="button"
              className="btn btn-danger"
              disabled={(layer.info.phase === null) && (this.props.selectedPhase === 1) && (data[layer.info.type].learn)}
              style={{ marginLeft: '80px', marginTop: '50px' }}
              onClick={() => this.props.deleteLayer(this.props.selectedLayer)}
            >
              Delete this layer
            </button>
            {trainOnlyCheckBox}
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
  trainOnly: React.PropTypes.func,
  selectedPhase: React.PropTypes.number,
  copyTrain: React.PropTypes.func,
};

export default SetParams;
