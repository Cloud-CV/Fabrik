import React from 'react';

class ModelElement extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    if (this.props.children){
      return (
      <a
        style={{color: "#848a92"}}
        className="btn"
        onClick={() => this.props.importNet('sample'+this.props.framework, this.props.id)}
        >
        {this.props.children}
      </a>
    );
    }
    else
      return null
  }
}

ModelElement.propTypes = {
  importNet: React.PropTypes.func,
  framework: React.PropTypes.string.isRequired,
  children: React.PropTypes.string.isRequired,
  id: React.PropTypes.string.isRequired
};

export default ModelElement;
