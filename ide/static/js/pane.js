import React from 'react';
import PaneElement from './paneElement';

function Pane() {
  return (

<li className="dropdown" id="pane-dropdown" style={{paddingTop:'4px'}}>
  <button data-toggle="dropdown" className="dropdown-toggle" aria-haspopup="true" 
  aria-expanded="true"><span className="glyphicon glyphicon-plus-sign" style={{fontSize:'24px'}}></span></button>

  <ul className="dropdown-menu" id="addLayerDropdown">
    <li className="dropdown-submenu">
      <a tabIndex="-1" href="#">Data Layers</a>
      <ul className="dropdown-menu">
        <li><PaneElement id="ImageData">ImageData</PaneElement></li>
        <li><PaneElement id="Data">Data</PaneElement></li>
        <li><PaneElement id="HDF5Data">HDF5Data</PaneElement></li>
        <li><PaneElement id="HDF5Output">HDF5Output</PaneElement></li>
        <li><PaneElement id="Input">Input</PaneElement></li>
        <li><PaneElement id="WindowData">WindowData</PaneElement></li>
        <li><PaneElement id="MemoryData">MemoryData</PaneElement></li>
        <li><PaneElement id="DummyData">DummyData</PaneElement></li>
      </ul>
    </li>
    <li className="dropdown-submenu">
      <a tabIndex="-1" href="#">Vision Layers</a>
      <ul className="dropdown-menu">
        <li><PaneElement id="Convolution">Convolution</PaneElement></li>
        <li><PaneElement id="Pooling">Pool</PaneElement></li>
        <li><PaneElement id="SPP">SPP</PaneElement></li>
        <li><PaneElement id="Crop">Crop</PaneElement></li>
        <li><PaneElement id="Deconvolution">Deconvolution</PaneElement></li>
      </ul>
    </li>
    <li className="dropdown-submenu">
      <a tabIndex="-1" href="#">Recurrent Layers</a>
      <ul className="dropdown-menu">
        <li><PaneElement id="Recurrent">Recurrent</PaneElement></li>
        <li><PaneElement id="RNN">RNN</PaneElement></li>
        <li><PaneElement id="LSTM">LSTM</PaneElement></li>
      </ul>
    </li>
    <li className="dropdown-submenu">
      <a tabIndex="-1" href="#">Common Layers</a>
      <ul className="dropdown-menu">
        <li><PaneElement id="InnerProduct">Inner Product</PaneElement></li>
        <li><PaneElement id="Dropout">Dropout</PaneElement></li>
        <li><PaneElement id="Embed">Embed</PaneElement></li>
      </ul>
    </li>
    <li className="dropdown-submenu">
      <a tabIndex="-1" href="#">Normalisation Layers</a>
      <ul className="dropdown-menu">
        <li><PaneElement id="LRN">LRN</PaneElement></li>
        <li><PaneElement id="MVN">MVN</PaneElement></li>
        <li><PaneElement id="BatchNorm">Batch Norm</PaneElement></li>
      </ul>
    </li>
    <li className="dropdown-submenu">
      <a tabIndex="-1" href="#">Activation/Neuron Layers</a>
      <ul className="dropdown-menu">
        <li><PaneElement id="ReLU">ReLU/Leaky-ReLU</PaneElement></li>
        <li><PaneElement id="PReLU">PReLU</PaneElement></li>
        <li><PaneElement id="ELU">ELU</PaneElement></li>
        <li><PaneElement id="Sigmoid">Sigmoid</PaneElement></li>
        <li><PaneElement id="TanH">TanH</PaneElement></li>
        <li><PaneElement id="AbsVal">Absolute Value</PaneElement></li>
        <li><PaneElement id="Power">Power</PaneElement></li>
        <li><PaneElement id="Exp">Exp</PaneElement></li>
        <li><PaneElement id="Log">Log</PaneElement></li>
        <li><PaneElement id="BNLL">BNLL</PaneElement></li>
        <li><PaneElement id="Threshold">Threshold</PaneElement></li>
        <li><PaneElement id="Bias">Bias</PaneElement></li>
        <li><PaneElement id="Scale">Scale</PaneElement></li>
      </ul>
    </li>
    <li className="dropdown-submenu">
      <a tabIndex="-1" href="#">Utility Layers</a>
      <ul className="dropdown-menu">
        <li><PaneElement id="Flatten">Flatten</PaneElement></li>
        <li><PaneElement id="Reshape">Reshape</PaneElement></li>
        <li><PaneElement id="BatchReindex">Batch Reindex</PaneElement></li>
        <li><PaneElement id="Split">Split</PaneElement></li>
        <li><PaneElement id="Concat">Concat</PaneElement></li>
        <li><PaneElement id="Eltwise">Eltwise</PaneElement></li>
        <li><PaneElement id="Filter">Filter</PaneElement></li>
        <li><PaneElement id="Parameter">Parameter</PaneElement></li> 
        <li><PaneElement id="Reduction">Reduction</PaneElement></li>
        <li><PaneElement id="Silence">Silence</PaneElement></li>
        <li><PaneElement id="ArgMax">ArgMax</PaneElement></li>
        <li><PaneElement id="Softmax">Softmax</PaneElement></li>
      </ul>
    </li>
    <li className="dropdown-submenu">
      <a tabIndex="-1" href="#">Loss Layers</a>
      <ul className="dropdown-menu">
        <li><PaneElement id="MultinomialLogisticLoss">Multinomial Logistic Loss</PaneElement></li>
        <li><PaneElement id="InfogainLoss">Infogain Loss</PaneElement></li>
        <li><PaneElement id="SoftmaxWithLoss">Softmax With Loss</PaneElement></li>
        <li><PaneElement id="EuclideanLoss">Euclidean Loss</PaneElement></li>
        <li><PaneElement id="HingeLoss">Hinge Loss</PaneElement></li>
        <li><PaneElement id="SigmoidCrossEntropyLoss">Sigmoid Cross Entropy Loss</PaneElement></li>
        <li><PaneElement id="Accuracy">Accuracy</PaneElement></li>
        <li><PaneElement id="ContrastiveLoss">Contrastive Loss</PaneElement></li>
      </ul>
    </li>    
  </ul>
</li>


  );
}

export default Pane;