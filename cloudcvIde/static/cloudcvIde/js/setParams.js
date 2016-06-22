import React from 'react';
import Field from './field';
import data from './data';

class SetParams extends React.Component {
  constructor(props) {
    super(props);
    this.changeParams = this.changeParams.bind(this);
    this.changeProps = this.changeProps.bind(this);
  }
  changeProps(prop, value) {
    const net = this.props.net;
    const layer = net[this.props.selectedLayer];
    layer.props[prop].value = value;
    this.props.modifyLayer(layer);
  }
  changeParams(para, value) {
    const net = this.props.net;
    const layer = net[this.props.selectedLayer];
    layer.params[para].value = value;
    this.props.modifyLayer(layer);
  }
  render() {
    if (this.props.selectedLayer) {
      const params = [];
      const props = [];
      const layer = this.props.net[this.props.selectedLayer];

      Object.keys(layer.params).forEach(i =>
        params.push(
          <Field
            id={i}
            key={i}
            data={layer.params[i]}
            changeField={this.changeParams}
          />
        )
      );

      Object.keys(layer.props).forEach(i =>
        props.push(
          <Field
            id={i}
            key={i}
            data={layer.props[i]}
            changeField={this.changeProps}
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
              style={{ marginLeft: '80px', marginTop: '50px' }}
              onClick={this.props.deleteLayer}
            >
              Delete this layer
            </button>
          </div>
        </div>
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
      </div>
    );
  }
}

SetParams.propTypes = {
  selectedLayer: React.PropTypes.string,
  net: React.PropTypes.object,
  deleteLayer: React.PropTypes.func,
  modifyLayer: React.PropTypes.func,
};

export default SetParams;
