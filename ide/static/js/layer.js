import React from 'react';
import data from './data';
import CommentTooltip from './commentTooltip'
import AddCommentModal from './addCommentModal'

class Layer extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      addCommentModalIsOpen: false
    }
    this.onAddComment = this.onAddComment.bind(this);
    this.onCloseCommentModal = this.onCloseCommentModal.bind(this);
    this.doSharedUpdate = this.doSharedUpdate.bind(this);
    this.openCommentSidebar = this.openCommentSidebar.bind(this);
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
  doSharedUpdate(comment) {
    this.props.addSharedComment(this.props.id, comment);
  }
  openCommentSidebar() {
    this.props.changeCommentOnLayer(this.props.id);
  }
  render() {
    let comments = [];
    let addCommentModal = null;
    let commentButton = null;
    let highlightUser = null;
    let highlightClass = '';
    let highlightColor = '#000';
 

    if(this.props.layer.highlight && this.props.layer.highlight.length > 0) {
      highlightClass = 'highlighted';
      highlightColor = this.props.layer.highlightColor[this.props.layer.highlightColor.length - 1];
      highlightUser = (<div className="highlight-style" style={{background: highlightColor}}>
                            {this.props.layer.highlight[this.props.layer.highlight.length - 1]}
                        </div>);
    }
    if ('comments' in this.props.layer && this.props.layer['comments'].length > 0) {
      comments = (<CommentTooltip
                          comments={this.props.layer['comments']}
                          top={this.props.top}
                          doSharedUpdate = {this.doSharedUpdate}
                          openCommentSidebar = {this.openCommentSidebar}
                          />);
    }
    if (this.state.addCommentModalIsOpen) {
      addCommentModal = (<AddCommentModal
                                  layer={this.props.layer}
                                  onCloseCommentModal={this.onCloseCommentModal}
                                  doSharedUpdate={this.doSharedUpdate}/>);
    }

    if (this.props.isShared && !this.state.isForked && comments.length < 1) {
      commentButton = (<a style={{color: 'white', position: 'absolute', top: '-5px', right: '-1px'}}
                          onClick={(event) => this.onAddComment(event)}>
                            <span className="glyphicon glyphicon-comment"
                                  style={{ fontSize: '15px', paddingRight: '5px'}} aria-hidden="true">
                            </span>
                        </a>);
    }
    return (
      <div
        className={`layer ${this.props.class} ${highlightClass}`}
        id={this.props.id}
        style={{
          top:this.props.top,
          left:this.props.left,
          background: data[this.props.type].color,
          borderColor: highlightColor
        }}
        data-type={this.props.type}
        onClick={(event) => this.props.click(event, this.props.id)}
        onMouseEnter={(event) => this.props.hover(event, this.props.id)}
        onMouseUp={(event) => this.props.mouseUp(event, this.props.id)}
        data-tip='tooltip'
        data-for='getContent'
      >
        {commentButton}
        {comments}
        {addCommentModal}
        {data[this.props.type].name}
        {highlightUser}
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
  mouseUp: React.PropTypes.func,
  layer: React.PropTypes.object,
  net: React.PropTypes.object,
  addSharedComment: React.PropTypes.func,
  isShared: React.PropTypes.bool,
  isForked: React.PropTypes.bool,
  changeCommentOnLayer: React.PropTypes.func
};

export default Layer;
