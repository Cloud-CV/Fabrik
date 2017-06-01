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

    if (type === 'text') {
      inputElement = (
        <input
          type="text"
          disabled={this.props.disabled}
          value={this.props.value}
          className="form-control  tooltipField"
          id={this.props.id}
          onChange={this.change}
        />
      );
    } else if (type === 'number') {
      inputElement = (
        <input
          type="number"
          value={this.props.value}
          disabled={this.props.disabled}
          className="form-control  tooltipField"
          id={this.props.id}
          onChange={this.change}
        />
      );
    } else if (type === 'float') {
      inputElement = (
        <input
          type="number"
          step="0.01"
          disabled={this.props.disabled}
          value={this.props.value}
          className="form-control  tooltipField"
          id={this.props.id}
          onChange={this.change}
        />
      );
    } else if (type === 'select') {
      const options = [];
      this.props.data.options.forEach(i => {
        options.push(<option key={i} value={i}>{i}</option>);
      });
      inputElement = (
        <input
          value={this.props.value}
          id={this.props.id}
          disabled={this.props.disabled}
          className="form-control tooltipField selectField"
          onChange={this.change}
        >
        </input>
      );
    } else if (type === 'checkbox') {
      inputElement = (
        <input
          type="checkbox"
          disabled={this.props.disabled}
          checked={this.props.value}
          id={this.props.id}
          onChange={this.change}
        />
      );
    }

    return (
      <div className="form-group" id="tooltipData">
      <div className="row">
        <div className="col-sm-8 form-control tooltipLabel">
            {this.props.data.name}
        </div>
        <div className="col-sm-4   rhTooltip">
           {inputElement}
        </div>
        </div>
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
