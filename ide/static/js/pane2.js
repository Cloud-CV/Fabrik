import React from 'react';
import PaneElement from './paneElement';

function Pane() {
  return (

    <div className="panel-group" id="menu" role="tablist" aria-multiselectable="true">
          <div className="panel panel-default">
            <div className="panel-heading" role="tab"  id="dataLayers">
              <h4 className="panel-title">
                <a data-toggle="collapse" data-parent="#menu" href="#data" aria-expanded="false" aria-controls="data">
                  Data Layers
                </a>
              </h4>
            </div>
            <div id="data" className="panel-collapse collapse" role="tabpanel">
              <div className="panel-body">
                <PaneElement id="ImageData">ImageData</PaneElement>
                <PaneElement id="Data">Data</PaneElement>
                <PaneElement id="HDF5Data">HDF5Data</PaneElement>
                <PaneElement id="HDF5Output">HDF5Output</PaneElement>
                <PaneElement id="Input">Input</PaneElement>
                <PaneElement id="WindowData">WindowData</PaneElement>
                <PaneElement id="MemoryData">MemoryData</PaneElement>
                <PaneElement id="DummyData">DummyData</PaneElement>
                <PaneElement id="Python">Python</PaneElement>
              </div>
            </div>
          </div>
          <div className="panel panel-default">
            <div className="panel-heading" role="tab"  id="visionLayers">
              <h4 className="panel-title">
                <a data-toggle="collapse" data-parent="#menu" href="#vision" aria-expanded="false" aria-controls="vision">
                  Vision Layers
                </a>
              </h4>
            </div>
            <div id="vision" className="panel-collapse collapse" role="tabpanel">
              <div className="panel-body">
                <PaneElement id="Convolution">Convolution</PaneElement>
                <PaneElement id="Pooling">Pool</PaneElement>
                <PaneElement id="Upsample">Upsample</PaneElement>
                <PaneElement id="Locally Connected">LocallyConnected</PaneElement>
                <PaneElement id="Crop">Crop</PaneElement>
                <PaneElement id="SPP">SPP</PaneElement>
                <PaneElement id="Deconvolution">Deconvolution</PaneElement>
              </div>
            </div>
          </div>
          <div className="panel panel-default">
            <div className="panel-heading" role="tab"  id="recurrentLayers">
              <h4 className="panel-title">
                <a data-toggle="collapse" data-parent="#menu" href="#recurrent" aria-expanded="false" aria-controls="recurrent">
                  Recurrent Layers
                </a>
              </h4>
            </div>
            <div id="recurrent" className="panel-collapse collapse" role="tabpanel">
              <div className="panel-body">
                <PaneElement id="Recurrent">Recurrent</PaneElement>
                <PaneElement id="RNN">RNN</PaneElement>
                <PaneElement id="GRU">GRU</PaneElement>
                <PaneElement id="LSTM">LSTM</PaneElement>
              </div>
            </div>
          </div>
          <div className="panel panel-default">
            <div className="panel-heading" role="tab"  id="utilityLayers">
              <h4 className="panel-title">
                <a data-toggle="collapse" data-parent="#menu" href="#utility" aria-expanded="false" aria-controls="utility">
                  Utility Layers
                </a>
              </h4>
            </div>
            <div id="utility" className="panel-collapse collapse" role="tabpanel">
              <div className="panel-body">
                <PaneElement id="Flatten">Flatten</PaneElement>
                <PaneElement id="Reshape">Reshape</PaneElement>
                <PaneElement id="BatchReindex">Batch Reindex</PaneElement>
                <PaneElement id="Split">Split</PaneElement>
                <PaneElement id="Concat">Concat</PaneElement>
                <PaneElement id="Eltwise">Eltwise</PaneElement>
                <PaneElement id="Filter">Filter</PaneElement>
                <PaneElement id="Reduction">Reduction</PaneElement>
                <PaneElement id="Silence">Silence</PaneElement>
                <PaneElement id="ArgMax">ArgMax</PaneElement>
                <PaneElement id="Softmax">Softmax</PaneElement>
                <PaneElement id="Permute">Permute</PaneElement>
                <PaneElement id="RepeatVector">Repeat Vector</PaneElement>
                <PaneElement id="Regularization">Regularization</PaneElement>
                <PaneElement id="Masking">Masking</PaneElement>
              </div>
            </div>
          </div>
          <div className="panel panel-default">
            <div className="panel-heading" role="tab"  id="activationLayers">
              <h4 className="panel-title">
                <a data-toggle="collapse" data-parent="#menu" href="#activation" aria-expanded="false" aria-controls="activation">
                  Activation/Neuron Layers
                </a>
              </h4>
            </div>
            <div id="activation" className="panel-collapse collapse" role="tabpanel">
              <div className="panel-body">
                <PaneElement id="ReLU">ReLU/Leaky-ReLU</PaneElement>
                <PaneElement id="PReLU">PReLU</PaneElement>
                <PaneElement id="ELU">ELU</PaneElement>
                <PaneElement id="ThresholdedReLU">Thresholded ReLU</PaneElement>
                <PaneElement id="SELU">SELU</PaneElement>
                <PaneElement id="Softplus">Softplus</PaneElement>
                <PaneElement id="Softsign">Softsign</PaneElement>
                <PaneElement id="Sigmoid">Sigmoid</PaneElement>
                <PaneElement id="TanH">TanH</PaneElement>
                <PaneElement id="HardSigmoid">Hard Sigmoid</PaneElement>
                <PaneElement id="AbsVal">Absolute Value</PaneElement>
                <PaneElement id="Power">Power</PaneElement>
                <PaneElement id="Exp">Exp</PaneElement>
                <PaneElement id="Log">Log</PaneElement>
                <PaneElement id="BNLL">BNLL</PaneElement>
                <PaneElement id="Threshold">Threshold</PaneElement>
                <PaneElement id="Bias">Bias</PaneElement>
                <PaneElement id="Scale">Scale</PaneElement>
              </div>
            </div>
          </div>
          <div className="panel panel-default">
            <div className="panel-heading" role="tab"  id="normalizationLayers">
              <h4 className="panel-title">
                <a data-toggle="collapse" data-parent="#menu" href="#normalization" aria-expanded="false" aria-controls="normalization">
                  Normalisation Layers
                </a>
              </h4>
            </div>
            <div id="normalization" className="panel-collapse collapse" role="tabpanel">
              <div className="panel-body">
                <PaneElement id="LRN">LRN</PaneElement>
                <PaneElement id="MVN">MVN</PaneElement>
                <PaneElement id="BatchNorm">Batch Norm</PaneElement>
              </div>
            </div>
          </div>
          <div className="panel panel-default">
            <div className="panel-heading" role="tab"  id="commonLayers">
              <h4 className="panel-title">
                <a data-toggle="collapse" data-parent="#menu" href="#common" aria-expanded="false" aria-controls="common">
                  Common Layers
                </a>
              </h4>
            </div>
            <div id="common" className="panel-collapse collapse" role="tabpanel">
              <div className="panel-body">
                <PaneElement id="InnerProduct">Inner Product</PaneElement>
                <PaneElement id="Dropout">Dropout</PaneElement>
                <PaneElement id="Embed">Embed</PaneElement>
              </div>
            </div>
          </div>
          <div className="panel panel-default">
            <div className="panel-heading" role="tab"  id="noiseLayers">
              <h4 className="panel-title">
                <a data-toggle="collapse" data-parent="#menu" href="#noise" aria-expanded="false" aria-controls="noise">
                  Noise Layers
                </a>
              </h4>
            </div>
            <div id="noise" className="panel-collapse collapse" role="tabpanel">
              <div className="panel-body">
                <PaneElement id="GaussianNoise">Gaussian Noise</PaneElement>
                <PaneElement id="GaussianDropout">Gaussian Dropout</PaneElement>
                <PaneElement id="AlphaDropout">Alpha Dropout</PaneElement>
              </div>
            </div>
          </div>
          <div className="panel panel-default">
            <div className="panel-heading" role="tab"  id="lossLayers">
              <h4 className="panel-title">
                <a data-toggle="collapse" data-parent="#menu" href="#loss" aria-expanded="false" aria-controls="loss">
                  Loss Layers
                </a>
              </h4>
            </div>
            <div id="loss" className="panel-collapse collapse" role="tabpanel">
              <div className="panel-body">
                <PaneElement id="MultinomialLogisticLoss">Multinomial Logistic Loss</PaneElement>
                <PaneElement id="InfogainLoss">Infogain Loss</PaneElement>
                <PaneElement id="SoftmaxWithLoss">Softmax With Loss</PaneElement>
                <PaneElement id="EuclideanLoss">Euclidean Loss</PaneElement>
                <PaneElement id="HingeLoss">Hinge Loss</PaneElement>
                <PaneElement id="SigmoidCrossEntropyLoss">Sigmoid Cross Entropy Loss</PaneElement>
                <PaneElement id="Accuracy">Accuracy</PaneElement>
                <PaneElement id="ContrastiveLoss">Contrastive Loss</PaneElement>
                <PaneElement id="Python">Python</PaneElement>
              </div>
            </div>
          </div>
    </div>


  );
}

export default Pane;