import React from 'react';

class CommentSidebar extends React.Component {
  constructor(props) {
    super(props);
    this.close = this.close.bind(this);
    this.addComment = this.addComment.bind(this);
  }
  close() {
    this.props.changeCommentOnLayer(null);
  }
  addComment() {
    this.props.net[this.props.commentOnLayer]['comments'].push(this.refs.comment_text.value);
    this.props.addSharedComment(this.props.commentOnLayer, this.refs.comment_text.value);
    this.refs.comment_text.value = '';
  }
  render() {
    let commentDiv = [];
    if (this.props.commentOnLayer) {
      let comments = this.props.net[this.props.commentOnLayer]['comments'];
      for(var i=0; i<comments.length; i++) {
        commentDiv.push(
          <div key={i} style={{padding: '5px', margin: '10px', borderRadius: '3px', boxShadow: '0 4px 8px 0 rgba(0,0,0,0.2)'}}>
            <div className="row" style={{ paddingLeft: '20px'}}>
              <div className="col-md-2" style={{padding: '0px', paddingLeft: '6px'}}>
                <img src={'/static/img/user.png'} className="img-responsive" alt="user" height="30px" width="30px"/>
              </div>
              <div className="col-md-10" style={{padding: '0px', textAlign: 'left', paddingLeft: '5px' }}> Anonymous User</div>
            </div>
            <div className="row" style={{ paddingLeft: '20px', paddingTop: '2px'}}>
              <div className="col-md-12" style={{padding: '5px', textAlign: 'left',
                   height: 'auto', overflow: 'hidden', paddingLeft: '8px',
                   paddingRight: '20px', textOverflow: 'ellipsis'}}>
                {comments[i]}
              </div>
            </div>
          </div>
        );
      }

      return (
        <div className="setparams setparamsActive" >
          <div className="setHead">
            <h5 className="sidebar-heading">COMMENTS</h5>
            <h4>Input Layer</h4>
            <span className="glyphicon glyphicon-remove-sign closeSign" onClick={() => this.close()} aria-hidden="true"></span>
          </div>
          <div className="setContain">
            {commentDiv}
            <div className="row" style={{ paddingTop: '5px'}}>
              <div className="col-md-12" style={{ padding: '0px', paddingLeft: '24px', paddingRight: '0px', color: 'black'}}>
                <textarea ref="comment_text" className="CommentModalTextarea" placeholder="Add your comment here..."  onClick={this.handleClick}>
                </textarea>
              </div>
            </div>
            <div className="row" style={{ paddingTop: '5px', paddingLeft: '15px', paddingRight: '20px'}}>
              <div className="col-md-10" style={{padding: '0px', textAlign: 'left', float: 'right', paddingRight: '5px' }}>
                <button className="btn btn-success text-center pull-right" id='btn-comment' onClick={this.addComment}>
                    <span className="glyphicon glyphicon-comment" aria-hidden="true"></span> Comment
                </button>
              </div>
            </div>
          </div>
        </div>
      );
    }
    else {
      return (
        <div>
        </div>
      );
    }
  }
}

CommentSidebar.propTypes = {
  changeCommentOnLayer: React.PropTypes.func,
  commentOnLayer: React.PropTypes.string,
  net: React.PropTypes.object,
  addSharedComment: React.PropTypes.func
};

export default CommentSidebar;
