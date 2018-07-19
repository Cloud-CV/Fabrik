import React from 'react';

class CommentTooltip extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    let top=0;//parseInt(this.props.top.split('px')[0]);
    top += (this.props.index*60);
    top = top.toString() + 'px';
      return (
        <div className="commentTooltiptext" style={{ top: top }}>
          <div className="row" style={{ paddingLeft: '20px'}}>
            <div className="col-md-2" style={{padding: '0px', paddingLeft: '6px'}}>
              <img src={'/static/img/user.png'} className="img-responsive" alt="user" height="20px" width="20px"/>
            </div>
            <div className="col-md-10" style={{padding: '0px', textAlign: 'left', paddingLeft: '5px' }}> Anonymous User</div>
          </div>
          <div className="row" style={{ paddingLeft: '20px', paddingTop: '2px'}}>
            <div className="col-md-12" style={{padding: '0px', textAlign: 'left', paddingLeft: '6px' }}>
              {this.props.comment}
            </div>
          </div>
        </div>
      )
  }
}

CommentTooltip.propTypes = {
  comment: React.PropTypes.string.isRequired,
  top: React.PropTypes.string.isRequired,
  index: React.PropTypes.number.isRequired
};

export default CommentTooltip;
