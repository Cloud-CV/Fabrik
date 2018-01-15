import React from 'react';
import $ from 'jquery';

class UrlImportModal extends React.Component {
  constructor(props) {
    super(props);
    this.getTabClasses = this.getTabClasses.bind(this);
    this.import = this.import.bind(this);
    this.setUrl = this.setUrl.bind(this);
  }
  getTabClasses(framework) {
    let classes = 'url-import-modal-tab';
    if(framework === this.props.modelFramework) classes += ' selected';
    return classes;
  }
  import() {
    if(!$('.url-import-modal-tab.selected').length) {
      this.props.addError('You must select a framework to import!');
    }
    else {
      this.props.importNet('url', '');
    }
  }
  setUrl(e) {
    this.props.setModelUrl(e.target.value);
  }
  render() {
    return (
      <div className="url-import-modal">
        <h3>Load model from URL</h3>
        <div className="url-import-modal-tabs">
          <button className={this.getTabClasses('caffe')} onClick={this.props.setModelFramework} data-framework="caffe">Caffe</button>
          <button className={this.getTabClasses('keras')} onClick={this.props.setModelFramework} data-framework="keras">Keras</button>
          <button className={this.getTabClasses('tensorflow')} onClick={this.props.setModelFramework} data-framework="tensorflow">TensorFlow</button>
        </div>
        <textarea className="url-import-modal-input" onChange={this.setUrl} ></textarea>
        <div className="row">
          <button className="url-import-modal-button btn btn-default col-md-2 col-md-offset-5" onClick={this.import}>Import</button>
        </div>
      </div>
    );
  }
}

UrlImportModal.propTypes = {
  modelFramework: React.PropTypes.string,
  setModelFramework: React.PropTypes.func,
  importNet: React.PropTypes.func,
  addError: React.PropTypes.func,
  setModelUrl: React.PropTypes.func
};

export default UrlImportModal;
