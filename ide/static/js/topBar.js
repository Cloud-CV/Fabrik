import React from 'react';
import ModelElement from './modelElement';
import ReactTooltip from 'react-tooltip';

class TopBar extends React.Component {
  render() {
    return (
      <div className="topBar">
        <div className="row">
            <div className="col-md-3">
              <div className="form-group">
                  <div className="dropdown">
                    <button id="topbar-icon" className="btn btn-default dropdown-toggle form-control" data-toggle="dropdown" 
                    data-tip="Load from zoo">
                      <span className="glyphicon glyphicon-folder-open" aria-hidden="true"></span>
                    </button>
                    <ul className="dropdown-menu">
                      <li><ModelElement importNet={this.props.importNet} framework="caffe" id="alexnet">AlexNet</ModelElement></li>
                      <li><ModelElement importNet={this.props.importNet} framework="caffe" id="vgg16">VGG 16</ModelElement></li>
                      <li><ModelElement importNet={this.props.importNet} framework="caffe" id="GoogleNet">GoogLeNet</ModelElement></li>
                      <li><ModelElement importNet={this.props.importNet} framework="caffe" id="resnet101">ResNet 101</ModelElement></li>
                      <li><ModelElement importNet={this.props.importNet} framework="keras" id="v3">Inception V3</ModelElement></li>
                      <li><ModelElement importNet={this.props.importNet} framework="caffe" id="fcn">FCN32 Pascal</ModelElement></li>
                      <li><ModelElement importNet={this.props.importNet} framework="caffe" id="siamese_mnist">MNIST Siamese</ModelElement></li>
                      <li><ModelElement importNet={this.props.importNet} framework="caffe" id="All_CNN">All CNN</ModelElement></li>
                      <li><ModelElement importNet={this.props.importNet} framework="caffe" id="Squeezenet">Squeezenet</ModelElement></li>
                      <li><ModelElement importNet={this.props.importNet} framework="keras" id="textGeneration">Text Generation</ModelElement></li>
                      <li><ModelElement importNet={this.props.importNet} framework="keras" id="seq2seq_lang">Seq2Seq Translation</ModelElement></li>
                    </ul>
                  </div>
              </div>
            </div>
            <div className="col-md-3">
              <div className="form-group">
                <div className="dropdown">
                  <button id="topbar-icon" className="btn btn-default dropdown-toggle form-control" data-toggle="dropdown" data-tip="Export">
                    <span className="glyphicon glyphicon-export" aria-hidden="true"></span>
                  </button>
                  <ul className="dropdown-menu">
                    <li><a className="btn" href="#" onClick={() => this.props.exportNet('caffe')}>Caffe</a></li>
                    <li><a className="btn" href="#" onClick={() => this.props.exportNet('keras')}>Keras</a></li>
                    <li><a className="btn" href="#" onClick={() => this.props.exportNet('tensorflow')}>Tensorflow</a></li>
                  </ul>
                </div>
              </div>
            </div>
            <div className="col-md-3">
              <div className="form-group">
                <div className="dropdown">
                  <button id="topbar-icon" className="btn btn-default dropdown-toggle form-control" data-toggle="dropdown" data-tip="Import">
                    <span className="glyphicon glyphicon-import" aria-hidden="true"></span>
                  </button>
                  <ul className="dropdown-menu">
                    <li>
                        <a className="btn">
                        <label htmlFor="inputFilecaffe">Caffe</label>
                        <input id="inputFilecaffe" type="file" accept=".prototxt" onChange={() => this.props.importNet('caffe', '')}/>
                        </a>
                    </li>
                    <li>
                        <a className="btn">
                        <label htmlFor="inputFilekeras">Keras</label>
                        <input id="inputFilekeras" type="file" accept=".json" onChange={() => this.props.importNet('keras', '')}/>
                        </a>
                    </li>
                    <li>
                        <a className="btn">
                        <label htmlFor="inputFiletensorflow">Tensorflow</label>
                        <input id="inputFiletensorflow" type="file" accept=".pbtxt" onChange={() => this.props.importNet('tensorflow', '')}/>
                        </a>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            <div className="col-md-3">
              <div className="form-group">
                <button id="topbar-icon" className="btn btn-default dropdown-toggle form-control" data-toggle="dropdown" 
                onClick={() => this.props.saveDb()} data-tip="Share">
                    <span className="glyphicon glyphicon-share" aria-hidden="true"></span>
                </button>
              </div>
            </div>
        </div>
      <ReactTooltip type="dark" multiline={true}/>
      </div>
    );
  }
}

TopBar.propTypes = {
  exportNet: React.PropTypes.func,
  importNet: React.PropTypes.func,
  saveDb: React.PropTypes.func,
  loadDb: React.PropTypes.func
};

export default TopBar;
