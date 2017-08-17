import React from 'react';

class tooltipData extends React.Component {
  constructor(props) {
    super(props);
    this.change = this.change.bind(this);
  }
  change(e) {
    if (this.props.data.type === 'checkbox') {
      this.props.changeField(this.props.id, e.target.checked);
    } else {
      this.props.changeField(this.props.id, e.target.value);
    }
  }
  render() {
    const type = this.props.data.type;
    let inputElement;
    if (type == 'checkbox'){
      inputElement = this.props.value ? 'True' : 'False';
    }
    else{
      inputElement = this.props.value;
    }

    return (
      <div className="tooltipData">
        <p className="tooltipLabel">{this.props.data.name}:</p>
        <p className="tooltipField">{inputElement}</p>
      </div>
    );
  }
}

tooltipData.propTypes = {
  id: React.PropTypes.string.isRequired,
  data: React.PropTypes.object,
  changeField: React.PropTypes.func,
  value: React.PropTypes.oneOfType([
    React.PropTypes.string,
    React.PropTypes.number,
    React.PropTypes.bool
  ]),
  disabled: React.PropTypes.bool
};

export default tooltipData;
