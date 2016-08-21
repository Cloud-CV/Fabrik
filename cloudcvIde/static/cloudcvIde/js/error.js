import React from 'react';

class Error extends React.Component {
  constructor(props) {
    super(props);
    this.dismissError = this.dismissError.bind(this);
  }
  dismissError() {
    this.props.dismissError(this.props.index);
  }
  render() {
    return (
      <div className="error" style={{ top: this.props.index * 35 + 5 }}>
        <button type="button" className="close" onClick={this.dismissError}>
          <span aria-hidden="true">&times;</span>
        </button>
        {this.props.text}
      </div>
    );
  }
}

Error.propTypes = {
  text: React.PropTypes.string.isRequired,
  index: React.PropTypes.number,
  dismissError: React.PropTypes.func,
};

export default Error;
