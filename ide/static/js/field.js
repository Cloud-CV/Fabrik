import React from 'react';

class Field extends React.Component {
  constructor(props) {
    super(props);
    this.change = this.change.bind(this);
  }
  change(e) {
    if (this.props.data.type === 'checkbox') {
      this.props.changeField(this.props.id, e.target.checked);
    } else if(this.props.data.type === 'number') {
      this.props.changeField(this.props.id, Number(e.target.value));
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
          className="form-control"
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
          className="form-control"
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
          className="form-control"
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
        <select
          value={this.props.value}
          id={this.props.id}
          disabled={this.props.disabled}
          className="form-control"
          onChange={this.change}
        >
          {options}
        </select>
      );
    } else if (type === 'checkbox') {
      inputElement = (
        <div className="paramsCheckbox">
          <input
            type="checkbox"
            disabled={this.props.disabled}
            checked={this.props.value}
            id={this.props.id}
            onChange={this.change}
          />
          <label htmlFor={this.props.id}></label>
        </div>
      );
    }
    let displayStyle = "inherit";
    if (inputElement.props.className == 'paramsCheckbox'){
      displayStyle = "flex";
    }
    return (
      <div style={{display: displayStyle}}>
        <label htmlFor={this.props.id} className="sidebar-heading" style={{fontSize:"0.85em"}}>
          {this.props.data.name.toUpperCase()}
        </label>
           {inputElement}
      <br/>
      </div>
    );
  }
}

Field.propTypes = {
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

export default Field;
