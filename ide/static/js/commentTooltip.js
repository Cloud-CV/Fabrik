import React from 'react';

class CommentTooltip extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isModalOpen: false
    }
    this.handleClick = this.handleClick.bind(this);
    this.addComment = this.addComment.bind(this);
  }
  handleClick() {
    this.refs.comment_text.focus();
  }
  addComment() {
    this.props.comments.push(this.refs.comment_text.value);
    this.props.doSharedUpdate(this.refs.comment_text.value);
  }
  render() {
    let top=0;
    top = top.toString() + 'px';
    let comment = this.props.comments[0];
    let singleCommentTooltip = (<div className="commentTooltiptext" style={{ top: top }}>
                                  <div className="row" style={{ paddingLeft: '20px'}}>
                                    <div className="col-md-2" style={{padding: '0px', paddingLeft: '6px'}}>
                                      <img src={'/static/img/user.png'} className="img-responsive" alt="user" height="20px" width="20px"/>
                                    </div>
                                    <div className="col-md-10" style={{padding: '0px', textAlign: 'left', paddingLeft: '5px' }}> Anonymous User</div>
                                  </div>
                                  <div className="row" style={{ paddingLeft: '20px', paddingTop: '2px'}}>
                                    <div className="col-md-12" style={{padding: '0px', textAlign: 'left',
                                                                       height: '35px', overflow: 'hidden', paddingLeft: '8px',
                                                                       paddingRight: '20px', textOverflow: 'ellipsis'}}>
                                      {comment}
                                    </div>
                                  </div>
                                  <div className="row">
                                    <div className="col-md-5 col-md-offset-5" style={{padding: '0px', textAlign: 'right'}}>
                                      <a style={{color: 'white'}} onClick={this.props.openCommentSidebar}>
                                        <span className="glyphicon glyphicon-retweet"
                                            style={{ fontSize: '15px'}} aria-hidden="true">
                                        </span>
                                      </a>
                                    </div>
                                  </div>
                                </div>);

      if (this.state.isModalOpen) {
        let commentDiv = [];
        for(var i=0; i<this.props.comments.length; i++) {
          commentDiv.push(
            <div key={i}>
              <div className="row" style={{ paddingLeft: '20px'}}>
                <div className="col-md-2" style={{padding: '0px', paddingLeft: '6px'}}>
                  <img src={'/static/img/user.png'} className="img-responsive" alt="user" height="20px" width="20px"/>
                </div>
                <div className="col-md-10" style={{padding: '0px', textAlign: 'left', paddingLeft: '5px' }}> Anonymous User</div>
              </div>
              <div className="row" style={{ paddingLeft: '20px', paddingTop: '2px'}}>
                <div className="col-md-12" style={{padding: '0px', textAlign: 'left',
                     height: '35px', overflow: 'hidden', paddingLeft: '8px',
                     paddingRight: '20px', textOverflow: 'ellipsis'}}>
                  {this.props.comments[i]}
                </div>
              </div>
            </div>
          );
        }
      }

      return (
        <div>
          {singleCommentTooltip}
        </div>
      );
  }
}

CommentTooltip.propTypes = {
  comments: React.PropTypes.array.isRequired,
  top: React.PropTypes.string.isRequired,
  doSharedUpdate: React.PropTypes.func.isRequired,
  openCommentSidebar: React.PropTypes.func
};

export default CommentTooltip;
