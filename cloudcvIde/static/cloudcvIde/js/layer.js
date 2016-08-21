/* eslint max-len: ["warn", 80]*/
import React from 'react';
import data from './data';

class Layer extends React.Component {
  componentDidMount() {
    instance.addLayerEndpoints(this.props.id,
      data[this.props.type].endpoint.src,
      data[this.props.type].endpoint.trg
    );
  }
  componentWillUnmount() {
    instance.deleteEndpoint(`${this.props.id}-s0`);
    instance.deleteEndpoint(`${this.props.id}-t0`);
  }
  render() {
    return (
      <div
        className={`layer ${this.props.class}`}
        id={this.props.id}
        style={{
          top:this.props.top,
          left:this.props.left,
          background: data[this.props.type].color,
        }}
        data-type={this.props.type}
        onClick={(event) => this.props.click(event, this.props.id)}
      >
        {data[this.props.type].name}
      </div>
    );
  }
}

Layer.propTypes = {
  id: React.PropTypes.string.isRequired,
  type: React.PropTypes.string.isRequired,
  top: React.PropTypes.string.isRequired,
  left: React.PropTypes.string.isRequired,
  class: React.PropTypes.string,
  click: React.PropTypes.func,
};

export default Layer;
