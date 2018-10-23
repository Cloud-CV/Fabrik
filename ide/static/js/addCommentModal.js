import React from 'react';

class AddCommentModal extends React.Component {
  constructor(props) {
    super(props);
    this.addComment = this.addComment.bind(this);
    this.handleClick = this.handleClick.bind(this);
  }
  handleClick() {
    this.refs.comment.focus();
  }
  addComment(event) {
    if (!('comments' in this.props.layer)) {
      this.props.layer['comments'] = [];
    }
    this.props.layer['comments'].push(this.refs.comment.value);
    this.props.onCloseCommentModal(event);
    this.props.doSharedUpdate(this.refs.comment.value);
  }

  render() {
      return (
        <div className="addCommentTooltiptext" style={{ textAlign: 'left', color: "#000"}}>
          <div className="row" style={{ paddingLeft: '15px', paddingRight: '10px'}}>
            <div className="col-md-2" style={{padding: '0px', paddingLeft: '6px'}}>
              <img src={'/static/img/user.png'} className="img-responsive" alt="user" height="40px" width="40px"/>
            </div>
            <div className="col-md-10" style={{ padding: '0px', paddingLeft: '10px'}}>
              <textarea ref="comment" className="CommentTextarea" placeholder="Add your comment here..."  onClick={this.handleClick}>
              </textarea>
            </div>
          </div>
          <div className="row" style={{ paddingTop: '5px',paddingLeft: '15px', paddingRight: '20px'}}>
            <div className="col-md-2">
              <button onClick={this.props.onCloseCommentModal}>
                  <span className="glyphicon glyphicon-remove" style={{color: '#fff', fontSize: '18px', paddingTop: '8px'}} aria-hidden="true"></span>
              </button>
            </div>
            <div className="col-md-8" style={{padding: '0px', textAlign: 'left', float: 'right' }}>
              <button className="btn btn-success text-center pull-right" id='btn-comment' onClick={this.addComment}>
                  <span className="glyphicon glyphicon-comment" aria-hidden="true"></span> Comment
              </button>
            </div>
          </div>
        </div>
      )
  }
}

AddCommentModal.propTypes = {
  layer: React.PropTypes.object,
  onCloseCommentModal: React.PropTypes.func,
  doSharedUpdate: React.PropTypes.func
};

export default AddCommentModal;
