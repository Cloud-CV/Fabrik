import React from 'react';
import PaneElement from './paneElement';
import $ from 'jquery'

class Pane extends React.Component {
  constructor(props) {
        super(props);
        this.toggleClass= this.toggleClass.bind(this);
        this.state = {
            data: false,
            vision: false,
            recurrent: false,
            utility: false,
            activation: false,
            normalization: false,
            common: false,
            noise: false,
            loss: false,
            wrapper: false
        };
    }
    toggleClass() {
        var obj = {};
        for (var entry in this.state) {
            obj[entry] = $("#" + entry).attr("aria-expanded") === "true";
        }
        this.setState(obj);
    }
    componentDidMount() {
      let filter = (pattern) => {
        let layerCompability = (searchQuery, layerName) => {
          let j = 0;
          let seq = [];
          let full_match = true;
          for (let i = 0; i < searchQuery.length; i++) {
            while (j < layerName.length && layerName[j].toLowerCase() != searchQuery[i].toLowerCase()) {
              seq[j] = false;
              j++;
            }
            if (j < layerName.length && layerName[j].toLowerCase() == searchQuery[i].toLowerCase()) {
              seq[j] = true;
              j++;
            } else {
              full_match = false;
            }
          }
          return {
            match: seq,
            full_match: full_match 
          };
        }
        for (let elem of $('.drowpdown-button')) {
          let sub = elem.innerText;
          if (!sub) continue;
          let resp = layerCompability(pattern, sub);
          if (resp.full_match) {
            elem.style.display = 'block';
            let final = '';
            for (let i = 0; i < sub.length; i++) {
              if (resp.match[i]) {
                final += '<span class="matched-search-char">' + sub[i] + '</span>'
              } else {
                final += sub[i];
              }
            }
            elem.innerHTML = final;
          } else {
            elem.style.display = 'none';
          }
        }
        for (let elem of $('.panel-heading')) {
          let _p = pattern ? 'false' : 'true';
          if (elem.getAttribute('aria-expanded') == _p) {
            elem.click();
          }
        }
      }
      $('#layer-search-input').keyup((e) => {
        filter(e.target.value); 
      });
    }

    render() {
      return (
        <div className="panel-group" id="menu" role="tablist" aria-multiselectable="true">
              <div className="panel panel-default">
                <div href="#data" data-toggle="collapse" aria-expanded="false" aria-controls="data"
                className="panel-heading" role="tab"  onClick={() => this.toggleClass('data')}>
                    <a data-parent="#menu"  >
                    <span className="badge sidebar-badge" id="dataLayers"> </span>
                      Data
                      <span className={this.state.data ? 'glyphicon sidebar-dropdown glyphicon-menu-down':
                      'glyphicon sidebar-dropdown glyphicon-menu-right'}></span>
                    </a>
                </div>
                <div id="data" className="panel-collapse collapse" role=" tabpanel">
                  <div className="panel-body">
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="ImageData_Button">Image Data</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Data_Button">Data</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="HDF5Data_Button">HDF5 Data</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="HDF5Output_Button">HDF5 Output</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Input_Button">Input</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="WindowData_Button">Window Data</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="MemoryData_Button">Memory Data</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="DummyData_Button">Dummy Data</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Python_Button">Python</PaneElement>
                  </div>
                </div>
              </div>
              <div className="panel panel-default">
                <div className="panel-heading" role="tab" data-toggle="collapse"  href="#vision"
                aria-expanded="false" aria-controls="vision" onClick={() => this.toggleClass('vision')}>
                    <a data-parent="#menu">
                    <span className="badge sidebar-badge" id="visionLayers"> </span>
                      Vision
                      <span className={this.state.vision ? 'glyphicon sidebar-dropdown glyphicon-menu-down':
                      'glyphicon sidebar-dropdown glyphicon-menu-right'} ></span>
                    </a>
                </div>
                <div id="vision" className="panel-collapse collapse" role="tabpanel">
                  <div className="panel-body">
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Convolution_Button">Convolution</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Pooling_Button">Pool</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Upsample_Button">Upsample</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="LocallyConnected_Button">Locally Connected</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Crop_Button">Crop</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="SPP_Button">SPP</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Deconvolution_Button">Deconvolution</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="DepthwiseConv_Button">Depthwise Convolution</PaneElement>
                  </div>
                </div>
              </div>
              <div className="panel panel-default">
                <div className="panel-heading" role="tab" data-toggle="collapse"  href="#recurrent"
                aria-expanded="false" aria-controls="recurrent" onClick={() => this.toggleClass('recurrent')}>

                    <a data-parent="#menu" >
                    <span className="badge sidebar-badge" id="recurrentLayers"> </span>
                      Recurrent
                      <span className={this.state.recurrent ? 'glyphicon sidebar-dropdown glyphicon-menu-down':
                      'glyphicon sidebar-dropdown glyphicon-menu-right'} ></span>
                    </a>
                </div>
                <div id="recurrent" className="panel-collapse collapse" role="tabpanel">
                  <div className="panel-body">
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Recurrent_Button">Recurrent</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="RNN_Button">RNN</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="GRU_Button">GRU</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="LSTM_Button">LSTM</PaneElement>
                  </div>
                </div>
              </div>
              <div className="panel panel-default">
                <div className="panel-heading" role="tab" data-toggle="collapse" href="#utility"
                aria-expanded="false" aria-controls="utility" onClick={() => this.toggleClass('utility')}>

                    <a  data-parent="#menu">
                    <span className="badge sidebar-badge" id="utilityLayers"> </span>
                      Utility
                      <span className={this.state.utility ? 'glyphicon sidebar-dropdown glyphicon-menu-down':
                      'glyphicon sidebar-dropdown glyphicon-menu-right'}></span>
                    </a>
                </div>
                <div id="utility" className="panel-collapse collapse" role="tabpanel">
                  <div className="panel-body">
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Flatten_Button">Flatten</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Reshape_Button">Reshape</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="BatchReindex_Button">Batch Reindex</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Split_Button">Split</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Concat_Button">Concat</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Eltwise_Button">Eltwise</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Filter_Button">Filter</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Reduction_Button">Reduction</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Silence_Button">Silence</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="ArgMax_Button">ArgMax</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Softmax_Button">Softmax</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Permute_Button">Permute</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="RepeatVector_Button">Repeat Vector</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Regularization_Button">Regularization</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Masking_Button">Masking</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Slice_Button">Slice</PaneElement>
                  </div>
                </div>
              </div>
              <div className="panel panel-default">
                <div data-toggle="collapse"  href="#activation" aria-expanded="false" aria-controls="activation"
                className="panel-heading" role="tab" onClick={() => this.toggleClass('activation')}>
                    <a data-parent="#menu" >
                    <span className="badge sidebar-badge" id="activationLayers"> </span>
                      Activation/Neuron
                      <span className={this.state.activation ? 'glyphicon sidebar-dropdown glyphicon-menu-down':
                      'glyphicon sidebar-dropdown glyphicon-menu-right'} ></span>
                    </a>
                </div>
                <div id="activation" className="panel-collapse collapse" role="tabpanel">
                  <div className="panel-body">
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="ReLU_Button">ReLU/Leaky-ReLU</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="PReLU_Button">PReLU</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="ELU_Button">ELU</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="ThresholdedReLU">Thresholded ReLU</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="SELU_Button">SELU</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Softplus_Button">Softplus</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Softsign_Button">Softsign</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Sigmoid_Button">Sigmoid</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="TanH_Button">TanH</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="HardSigmoid_Button">Hard Sigmoid</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="AbsVal_Button">Absolute Value</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Power_Button">Power</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Exp_Button">Exp</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Log_Button">Log</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="BNLL_Button">BNLL</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Threshold_Button">Threshold</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Bias_Button">Bias</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Scale_Button">Scale</PaneElement>
                  </div>
                </div>
              </div>
              <div className="panel panel-default">
                <div className="panel-heading" role="tab" data-toggle="collapse" href="#normalization"
                aria-expanded="false" aria-controls="normalization" onClick={() => this.toggleClass('normalization')}>
                    <a  data-parent="#menu" >
                    <span className="badge sidebar-badge" id="normalizationLayers"> </span>
                      Normalization
                      <span className={this.state.normalization ? 'glyphicon sidebar-dropdown glyphicon-menu-down':
                      'glyphicon sidebar-dropdown glyphicon-menu-right'} ></span>
                    </a>
                </div>
                <div id="normalization" className="panel-collapse collapse" role="tabpanel">
                  <div className="panel-body">
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="LRN_Button">LRN</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="MVN_Button">MVN</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="BatchNorm_Button">Batch Norm</PaneElement>
                  </div>
                </div>
              </div>
              <div className="panel panel-default">
                <div className="panel-heading" role="tab" data-toggle="collapse"  href="#common" aria-expanded="false"
                aria-controls="common" onClick={() => this.toggleClass('common')}>
                    <a data-parent="#menu">
                    <span className="badge sidebar-badge" id="commonLayers"> </span>
                      Common
                      <span className={this.state.common ? 'glyphicon sidebar-dropdown glyphicon-menu-down':
                      'glyphicon sidebar-dropdown glyphicon-menu-right'} ></span>
                    </a>
                </div>
                <div id="common" className="panel-collapse collapse" role="tabpanel">
                  <div className="panel-body">
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="InnerProduct_Button">Inner Product</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Dropout_Button">Dropout</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Embed_Button">Embed</PaneElement>
                  </div>
                </div>
              </div>
              <div className="panel panel-default">
                <div className="panel-heading" role="tab" data-toggle="collapse"  href="#noise" aria-expanded="false"
                aria-controls="noise" onClick={() => this.toggleClass('noise')}>

                    <a data-parent="#menu" >
                    <span className="badge sidebar-badge" id="noiseLayers"> </span>
                      Noise

                      <span className={this.state.noise ? 'glyphicon sidebar-dropdown glyphicon-menu-down':
                      'glyphicon sidebar-dropdown glyphicon-menu-right'}></span>
                    </a>
                </div>
                <div id="noise" className="panel-collapse collapse" role="tabpanel">
                  <div className="panel-body">
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="GaussianNoise_Button">Gaussian Noise</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="GaussianDropout_Button">Gaussian Dropout</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="AlphaDropout_Button">Alpha Dropout</PaneElement>
                  </div>
                </div>
              </div>
              <div className="panel panel-default">
                <div className="panel-heading" role="tab" data-toggle="collapse" href="#loss" aria-expanded="false"
                aria-controls="loss" onClick={() => this.toggleClass('loss')}>
                    <a  data-parent="#menu">
                    <span className="badge sidebar-badge" id="lossLayers"> </span>
                      Loss
                      <span className={this.state.loss ? 'glyphicon sidebar-dropdown glyphicon-menu-down':
                      'glyphicon sidebar-dropdown glyphicon-menu-right'} ></span>
                    </a>
                </div>
                <div id="loss" className="panel-collapse collapse" role="tabpanel">
                  <div className="panel-body">
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="MultinomialLogisticLoss_Button">Multinomial Logistic Loss</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="InfogainLoss_Button">Infogain Loss</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="SoftmaxWithLoss_Button">Softmax With Loss</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="EuclideanLoss_Button">Euclidean Loss</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="HingeLoss_Button">Hinge Loss</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="SigmoidCrossEntropyLoss_Button">Sigmoid Cross Entropy Loss</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Accuracy_Button">Accuracy</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="ContrastiveLoss_Button">Contrastive Loss</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Python_Button">Python</PaneElement>
                  </div>
                </div>
              </div>
              <div className="panel panel-default">
                <div className="panel-heading" role="tab" data-toggle="collapse" href="#wrapper" aria-expanded="false"
                aria-controls="wrapper" onClick={() => this.toggleClass('wrapper')}>
                    <a  data-parent="#menu">
                    <span className="badge sidebar-badge" id="wrapperLayers"> </span>
                      Wrapper
                      <span className={this.state.wrapper ? 'glyphicon sidebar-dropdown glyphicon-menu-down':
                      'glyphicon sidebar-dropdown glyphicon-menu-right'} ></span>
                    </a>
                </div>
                <div id="wrapper" className="panel-collapse collapse" role="tabpanel">
                  <div className="panel-body">
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="TimeDistributed_Button">Time Distributed</PaneElement>
                    <PaneElement setDraggingLayer={this.props.setDraggingLayer}
                      handleClick={this.props.handleClick}
                      id="Bidirectional_Button">Bidirectional</PaneElement>
                  </div>
                </div>
              </div>
        </div>


      );
  }
}
Pane.propTypes = {
  handleClick: React.PropTypes.func.isRequired,
  setDraggingLayer: React.PropTypes.func.isRequired
};
export default Pane;
