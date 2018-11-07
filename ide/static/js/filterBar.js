import React from 'react';
import $ from 'jquery'

class FilterBar extends React.Component {
  constructor(props) {
        super(props);
        this.changeEvent= this.changeEvent.bind(this);
    }

changeEvent(cbid) {
      var kerasLayers = ["RNN_Button", "GRU_Button", "LSTM_Button", "Embed_Button", "ELU_Button", "Sigmoid_Button",
      "ThresholdedReLU", "ReLU_Button", "PReLU_Button", "Softmax_Button", "BatchNorm_Button", "SELU_Button",
      "GaussianNoise_Button", "GaussianDropout_Button", "AlphaDropout_Button", "TimeDistributed_Button", "TanH_Button",
      "Bidirectional_Button", "RepeatVector_Button", "Masking_Button", "Permute_Button", "InnerProduct_Button",
      "Deconvolution_Button", "Regularization_Button", "Softsign_Button", "Upsample_Button", "Pooling_Button",
      "LocallyConnected_Button", "Input_Button", "Convolution_Button", "LRN_Button", "DepthwiseConv_Button", "Flatten_Button",
      "Reshape_Button", "Concat_Button", "Softplus_Button", "HardSigmoid_Button", "Dropout_Button", "Eltwise_Button"];

      var tensorFlowLayers = ["Input_Button", "Convolution_Button", "Pooling_Button", "DepthwiseConv_Button", "InnerProduct_Button",
      "LRN_Button", "Concat_Button", "Flatten_Button", "BatchNorm_Button", "Deconvolution_Button", "Sigmoid_Button", 
      "Softplus_Button", "Softsign_Button", "ELU_Button", "ReLU_Button", "Softmax_Button", "TanH_Button", "SELU_Button",
      "Dropout_Button", "Eltwise_Button"];

      var caffeLayers = ["ImageData_Button", "HDF5Data_Button", "HDF5Output_Button", "Input_Button", "WindowData_Button",
      "MemoryData_Button", "DummyData_Button", "Convolution_Button", "Pooling_Button", "SPP_Button", "Deconvolution_Button",
      "Recurrent_Button", "RNN_Button", "LSTM_Button", "LRN_Button", "MVN_Button", "BatchNorm_Button",
      "InnerProduct_Button", "Dropout_Button", "Embed_Button", "ReLU_Button", "PReLU_Button", "ELU_Button",
      "Sigmoid_Button", "TanH_Button", "AbsVal_Button", "Power_Button", "Exp_Button", "Log_Button", "BNLL_Button",
      "Threshold_Button", "Bias_Button", "Scale_Button", "Flatten_Button", "ThresholdedReLU", "Python_Button",
      "Reshape_Button", "BatchReindex_Button", "Split_Button", "Concat_Button", "Eltwise_Button", "Filter_Button",
      "Reduction_Button", "Silence_Button", "ArgMax_Button", "Softmax_Button", "MultinomialLogisticLoss_Button",
      "InfogainLoss_Button", "SoftmaxWithLoss_Button", "EuclideanLoss_Button", "HingeLoss_Button", "Slice_Button",
      "SigmoidCrossEntropyLoss_Button", "Accuracy_Button", "ContrastiveLoss_Button", "Data_Button", "Crop_Button"];
      var filterCheckBox_Keras = document.getElementById("filterCheckBox_Keras");
      var filterCheckBox_TensorFlow = document.getElementById("filterCheckBox_TensorFlow");
      var filterCheckBox_Caffe = document.getElementById("filterCheckBox_Caffe");
      var visible = [];

    let checkBox = document.getElementById(cbid);
    checkBox.checked = !checkBox.checked;

      if (filterCheckBox_Keras.checked == false & filterCheckBox_TensorFlow.checked == false & filterCheckBox_Caffe.checked == false) {
        for (let elem of $('.drowpdown-button')) {
        elem.classList.remove("hide");
        }            
      }
      if (filterCheckBox_Keras.checked == true) {
         visible = visible.concat(kerasLayers);
      }
      if (filterCheckBox_TensorFlow.checked == true) {
         visible = visible.concat(tensorFlowLayers);
      }
      if (filterCheckBox_Caffe.checked == true) {
         visible = visible.concat(caffeLayers);
      }
      
            for (let elem of $('.drowpdown-button')) {
                for (let j = 0; j < visible.length; j++) {
                let id = elem.id;
                if (id == visible[j]) {
                    elem.classList.remove("hide");
                    j = visible.length + 1;
                }
                else {
                elem.classList.add("hide");
                }
            }
        }

    }

    render() {
      return (
            <div>
              <input id="layer-search-input" placeholder="Search for layer"></input>
              <i className="material-icons" id="layer-search-icon">search</i>
              <div className="form-group pull-right">
                <div className="dropdown">
                  <button id="topbar-icon" className="btn btn-default dropdown-toggle form-control filter-button" data-toggle="dropdown">
                    <span className="glyphicon glyphicon-filter filter-glyphicon" aria-hidden="true"></span>
                  </button>
                  <ul className="dropdown-menu pull-right">
                    <li>
                        <a className="btn" onClick={this.changeEvent.bind(this, "filterCheckBox_Keras")}>
                        <label className="filter">Keras</label>
                        <input type="checkBox" id="filterCheckBox_Keras" onClick={this.changeEvent.bind(this, "filterCheckBox_Keras")} />
                        </a>
                    </li>
                    <li>
                        <a className="btn" onClick={this.changeEvent.bind(this, "filterCheckBox_TensorFlow")}>
                        <label className="filter">Tensorflow</label>
                        <input type="checkBox" id="filterCheckBox_TensorFlow" onClick={this.changeEvent.bind(this, "filterCheckBox_TensorFlow")} />
                        </a>
                    </li>
                    <li>
                        <a className="btn" onClick={this.changeEvent.bind(this, "filterCheckBox_Caffe")}>
                        <label className="filter">Caffe</label>
                        <input type="checkBox" id="filterCheckBox_Caffe" onClick={this.changeEvent.bind(this, "filterCheckBox_Caffe")} />
                        </a>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
             )
    }
}
export default FilterBar;
