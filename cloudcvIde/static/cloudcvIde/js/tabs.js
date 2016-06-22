import React from 'react';

class Tabs extends React.Component {
  componentDidMount() {
    $('#phaseTabs a').click(e => {
      e.preventDefault();
      if (e.target.id === 'train') {
        this.props.changeNetPhase(0);
      } else if (e.target.id === 'test') {
        this.props.changeNetPhase(1);
      }
    });
  }
  render() {
    let tab;
    if (this.props.selectedPhase === 0) {
      tab = (<ul id="phaseTabs" className="nav nav-tabs" role="tablist">
        <li role="presentation" className="active"><a id="train">Train</a></li>
        <li role="presentation"><a id="test">Test</a></li>
      </ul>);
    } else if (this.props.selectedPhase === 1) {
      tab = (<ul id="phaseTabs" className="nav nav-tabs" role="tablist">
        <li role="presentation"><a id="train">Train</a></li>
        <li role="presentation" className="active"><a id="test">Test</a></li>
      </ul>);
    }
    return (
      <div className="row">
        <div className="col-md-7 col-md-offset-2">
          {tab}
        </div>
      </div>
    );
  }
}

Tabs.propTypes = {
  changeNetPhase: React.PropTypes.func,
  selectedPhase: React.PropTypes.number,
};

export default Tabs;
