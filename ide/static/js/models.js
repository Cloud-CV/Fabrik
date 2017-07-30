import React from 'react';
import ModelElement from './modelElement';

class Models extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (

      <li className="dropdown" id="model-dropdown">
        <button data-toggle="dropdown" className="dropdown-toggle btn btn-default" aria-haspopup="true" 
        aria-expanded="true">Models &#9660;</button>

        <ul className="dropdown-menu" id="addModelDropdown">
          <li className="dropdown-submenu">
            <a tabIndex="-1" href="#">Classification</a>
            <ul className="dropdown-menu">
              <li><ModelElement importNet={this.props.importNet} framework="caffe" id="alexnet">AlexNet</ModelElement></li>
              <li><ModelElement importNet={this.props.importNet} framework="caffe" id="vgg16">VGG 16</ModelElement></li>
              <li><ModelElement importNet={this.props.importNet} framework="caffe" id="GoogleNet">GoogLeNet</ModelElement></li>
              <li><ModelElement importNet={this.props.importNet} framework="caffe" id="resnet101">ResNet 101</ModelElement></li>
              <li><ModelElement importNet={this.props.importNet} framework="keras" id="v3">Inception V3</ModelElement></li>
            </ul>
          </li>  
          <li className="dropdown-submenu">
            <a tabIndex="-1" href="#">Segmentation</a>
            <ul className="dropdown-menu">
              <li><ModelElement importNet={this.props.importNet} framework="caffe" id="fcn">FCN32 Pascal</ModelElement></li>
            </ul>
          </li>
          <li className="dropdown-submenu">
            <a tabIndex="-1" href="#">Others</a>
            <ul className="dropdown-menu">
              <li><ModelElement importNet={this.props.importNet} framework="caffe" id="siamese_mnist">Mnist Siamese</ModelElement></li>
            </ul>
          </li>  
        </ul>
      </li>
    );
}
}

Models.propTypes = {
  importNet: React.PropTypes.func
};

export default Models;