import React from 'react';

class Error extends React.Component {
  render() {
    return (
      <div className="error" style={{'top':this.props.top.toString()}}>
        <button type="button" className="close" data-dismiss="alert" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
        {this.props.text}
      </div>
    );
  }
}

export default Error;
