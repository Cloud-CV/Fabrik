import React from 'react';

class Info extends React.Component {
  constructor(props) {
    super(props);
    this.dismissInfo = this.dismissInfo.bind(this);
  }
  dismissInfo() {
    this.props.dismissInfo(this.props.index);
  }
  render() {
    return (
      <div className="info">
        <button type="button" className="close" onClick={this.dismissInfo}>
          <span aria-hidden="true">&times;</span>
        </button>
        {this.props.content}
      </div>
    );
  }
}

Info.propTypes = {
  content: React.PropTypes.oneOfType([React.PropTypes.element, React.PropTypes.string]).isRequired,
  index: React.PropTypes.number,
  dismissInfo: React.PropTypes.func
};

export default Info;
