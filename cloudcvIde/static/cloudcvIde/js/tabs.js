import React from 'react';

class Tabs extends React.Component {
  componentDidMount() {
    $('#phaseTabs button').click(e => {
      e.preventDefault();
      if (e.target.id === 'train') {
        this.props.changeNetPhase(0);
      } else if (e.target.id === 'test') {
        this.props.changeNetPhase(1);
      }
    });
  }
  render() {
    let trainClass = '',
      testClass = '';
    if (this.props.selectedPhase === 0) {
      trainClass = 'focus active';
    } else if (this.props.selectedPhase === 1) {
      testClass = 'focus active';
    }
    return (
      <li className="btn-group" role="group" id="phaseTabs">
        <button type="button" id="train" className={"btn btn-default "+trainClass}>Train</button>
        <button type="button" id="test" className={"btn btn-default "+testClass}>Test</button>
      </li>
    );
  }
}

Tabs.propTypes = {
  changeNetPhase: React.PropTypes.func,
  selectedPhase: React.PropTypes.number,
};

export default Tabs;
