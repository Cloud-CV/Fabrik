import React from 'react';
import data from './data';
import CommentTooltip from './commentTooltip'
import AddCommentModal from './addCommentModal'
//import Modal from 'react-modal';
/*
const infoStyle = {
  content : {
    top                   : '50%',
    left                  : '50%',
    right                 : '60%',
    bottom                : 'auto',
    marginRight           : '-50%',
    transform             : 'translate(-50%, -50%)',
    borderRadius          : '8px',
    width                 : '500px',
    height                : '220px',
    backgroundColor       : '#555'
  },
  overlay: {
    zIndex                : 100
  }
};*/

class Layer extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      addCommentModalIsOpen: false
    }
    this.onAddComment = this.onAddComment.bind(this);
    this.onCloseCommentModal = this.onCloseCommentModal.bind(this);
    this.doSharedUpdate = this.doSharedUpdate.bind(this);
  }
  componentDidMount() {
    instance.addLayerEndpoints(this.props.id,
      data[this.props.type].endpoint.src,
      data[this.props.type].endpoint.trg
    );
  }
  componentWillUnmount() {
    instance.deleteEndpoint(`${this.props.id}-s0`);
    instance.deleteEndpoint(`${this.props.id}-t0`);
  }
  onCloseCommentModal(event) {
    this.setState({ addCommentModalIsOpen: false})
    event.stopPropagation();
  }
  onAddComment(event) {
    // open the comment tooltip
    this.setState({ addCommentModalIsOpen: true })
    event.stopPropagation();
  }
  doSharedUpdate() {
    this.props.performSharedUpdate(this.props.net, 'AddComment');
  }
  render() {
    let comments = [];
    let addCommentModal = null;
    let commentButton = null;
    if (this.props.layer['comments']) {
      for (var i=0;i<this.props.layer['comments'].length;i++) {
        comments.push(<CommentTooltip
                          key={i}
                          comment={this.props.layer['comments'][i]}
                          top={this.props.top}
                          index={i}/>);
      }
    }
    if (this.state.addCommentModalIsOpen) {
      addCommentModal = (<AddCommentModal
                                  layer={this.props.layer}
                                  onCloseCommentModal={this.onCloseCommentModal}
                                  doSharedUpdate={this.doSharedUpdate}/>);
    }

    if (this.props.isShared) {
      commentButton = (<a style={{color: 'white', position: 'absolute', top: '-5px', right: '-1px'}}
                          onClick={(event) => this.onAddComment(event)}>
                            <span className="glyphicon glyphicon-comment"
                                  style={{ fontSize: '15px', paddingRight: '5px'}} aria-hidden="true">
                            </span>
                        </a>);
    }
    return (
      <div
        className={`layer ${this.props.class}`}
        id={this.props.id}
        style={{
          top:this.props.top,
          left:this.props.left,
          background: data[this.props.type].color
        }}
        data-type={this.props.type}
        onClick={(event) => this.props.click(event, this.props.id)}
        onMouseEnter={(event) => this.props.hover(event, this.props.id)}
        data-tip='tooltip'
        data-for='getContent'
      >
          {commentButton}
          {comments}
          { addCommentModal }
        {data[this.props.type].name}
      </div>
    );
  }
}

Layer.propTypes = {
  id: React.PropTypes.string.isRequired,
  type: React.PropTypes.string.isRequired,
  top: React.PropTypes.string.isRequired,
  left: React.PropTypes.string.isRequired,
  class: React.PropTypes.string,
  click: React.PropTypes.func,
  hover: React.PropTypes.func,
  layer: React.PropTypes.object,
  net: React.PropTypes.object,
  performSharedUpdate: React.PropTypes.func,
  isShared: React.PropTypes.bool
};

export default Layer;
