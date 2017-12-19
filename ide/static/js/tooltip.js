import React from 'react';
import TooltipData from './tooltipData';
import data from './data';
import ReactTooltip from 'react-tooltip'

class Tooltip extends React.Component {
  constructor(props) {
    super(props);
  }
  
  componentDidUpdate() {
    ReactTooltip.rebuild();
  }
 
  render() {
    if (this.props.hoveredLayer && this.props.hoveredLayer in this.props.net) {
      const params = [];
      const props = [];
      const layer = this.props.net[this.props.hoveredLayer];

      Object.keys(data[layer.info.type].params).forEach(param => {
        params.push(
          <TooltipData
            id={param}
            key={param}
            data={data[layer.info.type].params[param]}
            value={layer.params[param][0]}
            disabled={(layer.info.phase === null) && (this.props.selectedPhase === 1) && (data[layer.info.type].learn)}
            changeField={this.changeParams}
          />
        );
      });

      Object.keys(data[layer.info.type].props).forEach(prop => {
        props.push(
          <TooltipData
            id={prop}
            key={prop}
            data={data[layer.info.type].props[prop]}
            value={layer.props[prop]}
            disabled={(layer.info.phase === null) && (this.props.selectedPhase === 1) && (data[layer.info.type].learn)}
            changeField={this.changeProps}
          />
        );
      });

      return (
        <ReactTooltip multiline={true} id='getContent' effect='solid' place='right' className='customTooltip'>
          <div style={{display: 'inline-grid'}}>
              {props}
              {params}
          </div>
        </ReactTooltip>
    )
}
     else return null;
  }
}

Tooltip.propTypes = {
  hoveredLayer: React.PropTypes.string,
  net: React.PropTypes.object,
  selectedPhase: React.PropTypes.number
};

export default Tooltip;
