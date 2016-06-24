import React from 'react';
import Field from './field';
import data from './data';

class SetParams extends React.Component {
  constructor(props) {
    super(props);
    this.changeParams = this.changeParams.bind(this);
    this.changeProps = this.changeProps.bind(this);
    this.copyLayerToTest = this.copyLayerToTest.bind(this);
  }
  changeProps(prop, value) {
    const net = this.props.net;
    let layer = net[this.props.selectedLayer];
    layer = JSON.parse(JSON.stringify(layer))
    layer.props[prop].value = value;
    this.props.modifyLayer(layer);
  }
  changeParams(para, value) {
    const net = this.props.net;
    let layer = net[this.props.selectedLayer];
    layer = JSON.parse(JSON.stringify(layer))
    layer.params[para].value = value;
    this.props.modifyLayer(layer);
  }
  copyLayerToTest(e){
    if(e.target.checked){
      this.props.copyLayerToTest();
    }
  }
  render() {
    if (this.props.selectedLayer) {
      const params = [];
      const props = [];
      const layer = this.props.net[this.props.selectedLayer];

      let copyLayerToTestCheckBox = null;
      if(this.props.selectedPhase == 0){
        copyLayerToTestCheckBox = (
          <div className="form-group" style={{ marginTop: '30px' }}>
            <label
              className="col-sm-6 control-label"
            >
              copy to test
            </label>
            <div className="col-sm-6">
              <input
                type="checkbox"
                onChange={this.copyLayerToTest}
              />
            </div>
          </div>
        );
      }

      Object.keys(layer.params).forEach(i =>
        params.push(
          <Field
            id={i}
            key={i}
            data={layer.params[i]}
            layer={layer}
            changeField={this.changeParams}
            selectedPhase={this.props.selectedPhase}
          />
        )
      );

      Object.keys(layer.props).forEach(i =>
        props.push(
          <Field
            id={i}
            key={i}
            data={layer.props[i]}
            layer={layer}
            changeField={this.changeProps}
            selectedPhase={this.props.selectedPhase}
          />
        )
      );

      return (
        <div className="col-md-3 setparams" >

          <div className="setHead" style={{ color: data[layer.info.type].color }}>
            {layer.props.name.value} layer selected
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
              disabled={(layer.info.phase==null)&&(this.props.selectedPhase==1)&&(data[layer.info.type].learn)}
              style={{ marginLeft: '80px', marginTop: '50px' }}
              onClick={() => this.props.deleteLayer(this.props.selectedLayer)}
            >
              Delete this layer
            </button>
            {copyLayerToTestCheckBox}
          </div>
        </div>
      );
    } else {

      let copyTrainButton = null;
      if(this.props.selectedPhase==1){
        copyTrainButton = (
          <button
            className="btn btn-primary"
            onClick={this.props.copyTrain}
            style={{marginLeft:'80px'}}
          >
            Copy train net
          </button>
        )
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
};

export default SetParams;
