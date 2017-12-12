import React from 'react';

class PaneElement extends React.Component {
  constructor(props) {
    super(props);
    this.drag = this.drag.bind(this);
  }
  drag(e) {
    e.dataTransfer.setData('element_type', e.target.id);
  }
  render() {
    return (
      <div
        className="btn btn-block drowpdown-button"
        draggable="true"
        onClickCapture={this.props.handleClick}        
        onDragStart={this.drag}
        id={this.props.id}
      >
        {this.props.children}
      </div>
    );
  }
}

PaneElement.propTypes = {
  id: React.PropTypes.string.isRequired,
  children: React.PropTypes.string.isRequired,
  handleClick: React.PropTypes.func.isRequired
};

export default PaneElement;
