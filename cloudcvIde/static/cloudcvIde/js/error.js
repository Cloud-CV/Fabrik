import React from 'react';

class Error extends React.Component {
  constructor(props) {
    super(props);
    this.dismissError = this.dismissError.bind(this);
  }
  dismissError() {
    this.props.dismissError(this.props.index)
  }
  render() {
    return (
      <div className="error" style={{'top':this.props.top}}>
        <button type="button" className="close" onClick={this.dismissError}>
          <span aria-hidden="true">&times;</span>
        </button>
        {this.props.text}
      </div>
    );
  }
}

export default Error;
