import React from 'react';

class ModelElement extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    if (this.props.children){
      return (
      <div
        className="btn btn-default btn-block"
        onClick={() => this.props.importNet('sample'+this.props.framework, this.props.id)}
        >
        {this.props.children}
      </div>
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
