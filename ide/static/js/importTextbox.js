import React from 'react';
import $ from 'jquery';

class ImportTextbox extends React.Component {
  constructor(props) {
    super(props);
    this.getTabClasses = this.getTabClasses.bind(this);
    this.importConfig = this.importConfig.bind(this);
  }
  getTabClasses(framework) {
    let classes = 'import-textbox-tab';
    if(framework === this.props.modelFramework) classes += ' selected';
    return classes;
  }
  importConfig() {
    if(!$('.import-textbox-tab.selected').length) {
      this.props.addError('You must select a framework to import!');
    }
    else {
      this.props.importNet('input', '');
    }
  }
  render() {
    return (
      <div className="import-textbox">
        <h3>Load Model From Text Input</h3>
        <div className="import-textbox-tabs">
          <button className={this.getTabClasses('caffe')} onClick={this.props.setModelFramework} data-framework="caffe">Caffe</button>
          <button className={this.getTabClasses('keras')} onClick={this.props.setModelFramework} data-framework="keras">Keras</button>
          <button className={this.getTabClasses('tensorflow')} onClick={this.props.setModelFramework} data-framework="tensorflow">TensorFlow</button>
        </div>
        <textarea className="import-textbox-input" onChange={this.props.setModelConfig} defaultValue={this.props.modelConfig}></textarea>
        <div className="row">
          <button className="import-textbox-button btn btn-default col-md-2 col-md-offset-5" onClick={this.importConfig}>Import</button>
        </div>
      </div>
    );
  }
}

ImportTextbox.propTypes = {
  modelConfig: React.PropTypes.string,
  modelFramework: React.PropTypes.string,
  setModelConfig: React.PropTypes.func,
  setModelFramework: React.PropTypes.func,
  importNet: React.PropTypes.func,
  addError: React.PropTypes.func
};

export default ImportTextbox;