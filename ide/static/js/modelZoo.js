import React from 'react';
import ModelElement from './modelElement';

class ModelZoo extends React.Component {
    constructor(props) {
    super(props);
    this.mouseClick = this.mouseClick.bind(this);
    }
    mouseClick(event, id) {
      this.refs.recognition.className = "hide";
      this.refs.detection.className = "hide";
      this.refs.retrieval.className = "hide";
      this.refs.seq2seq.className = "hide";
      this.refs.caption.className = "hide";
      this.refs.segmentation.className = "hide";
      this.refs.vqa.className = "hide";
      $('#sidebar-nav li a').removeClass();
      event.currentTarget.className = "bold";
      if (id == "all") {
        this.refs.recognition.className = " ";
        this.refs.detection.className = " ";
        this.refs.retrieval.className = " ";
        this.refs.seq2seq.className = " ";
        this.refs.caption.className = " ";
        this.refs.segmentation.className = " ";
        this.refs.vqa.className = " ";
      }
      else if (id == "recognition")
      {
          this.refs.recognition.className = " ";
      }
      else if (id == "detection")
      {
          this.refs.detection.className = " ";
      }
      else if (id == "retrieval")
      {
          this.refs.retrieval.className = " ";
      }
      else if (id == "seq2seq")
      {
          this.refs.seq2seq.className = " ";
      }
      else if (id == "caption")
      {
          this.refs.caption.className = " ";
      }
      else if (id == "segmentation")
      {
          this.refs.segmentation.className = " ";
      }
      else if (id == "vqa")
      {
          this.refs.vqa.className = " ";
      }
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
        for (let elem of $('.col-sm-6')) {
          let sub = elem.id;
          if (!sub) continue;
          let resp = layerCompability(pattern, sub);
          if (resp.full_match) {
            elem.style.display = 'block';
          } else {
            elem.style.display = 'none';
          }
        }
      }
      $('#model-search-input').keyup((e) => {
        filter(e.target.value);
      });
    }

  render() {

    return (
      <div className="sidebar-content">
        <div id="wrapper" className="toggle" ref="wrapper1">
          <div id="sidebar-wrapper">
            <ul id="sidebar-nav" className="sidebar-nav">
                <div className="filterbar-container">
                  <input id="model-search-input" placeholder="Search for model"></input>
                  <i className="material-icons" id="model-search-icon">search</i>
                </div>
              <li>
                <a className="bold" onClick={(event) => this.mouseClick(event, "all")}>All</a>
              </li>
              <li>
                <a onClick={(event) => this.mouseClick(event, "recognition")}>Recognition</a>
              </li>
              <li>
                <a onClick={(event) => this.mouseClick(event, "detection")}>Detection</a>
              </li>
              <li>
                <a onClick={(event) => this.mouseClick(event, "retrieval")}>Retrieval</a>
              </li>
              <li>
                <a onClick={(event) => this.mouseClick(event, "seq2seq")}>Seq2Seq</a>
              </li>
              <li>
                <a onClick={(event) => this.mouseClick(event, "caption")}>Caption</a>
              </li>
              <li>
                <a onClick={(event) => this.mouseClick(event, "segmentation")}>Segmentation</a>
              </li>
              <li>
                <a onClick={(event) => this.mouseClick(event, "vqa")}>VQA</a>
              </li>
            </ul>
          </div>
        </div>
      <div id="page-content-wrapper">
        <div className="row" ref="ContentPage">
          <div ref="recognition">
            <ModelElement importNet={this.props.importNet} framework="keras" id="zfnet" displayName="ZFNet"> </ModelElement>
            <ModelElement importNet={this.props.importNet} framework="caffe" id="resnext" displayName="ResNeXt"> </ModelElement>
            <ModelElement importNet={this.props.importNet} framework="caffe" id="lenet" displayName="MNIST LeNet"> </ModelElement>
            <ModelElement importNet={this.props.importNet} framework="caffe" id="cifar10_full" displayName="Cifar10 CNN"> </ModelElement>
            <ModelElement importNet={this.props.importNet} framework="caffe" id="alexnet" displayName="AlexNet"> </ModelElement>
            <ModelElement importNet={this.props.importNet} framework="caffe" id="All_CNN" displayName="All CNN"> </ModelElement>
            <ModelElement importNet={this.props.importNet} framework="caffe" id="vgg16" displayName="VGG 16"> </ModelElement>
            <ModelElement importNet={this.props.importNet} framework="caffe" id="densenet" displayName="DenseNet"> </ModelElement>
            <ModelElement importNet={this.props.importNet} framework="caffe" id="GoogleNet" displayName="GoogLeNet"> </ModelElement>
            <ModelElement importNet={this.props.importNet} framework="caffe" id="resnet101" displayName="ResNet 101"> </ModelElement>
            <ModelElement importNet={this.props.importNet} framework="keras" id="v3" displayName="Inception V3"> </ModelElement>
            <ModelElement importNet={this.props.importNet} framework="keras" id="v4" displayName="Inception V4"> </ModelElement>
            <ModelElement importNet={this.props.importNet} framework="caffe" id="Squeezenet" displayName="Squeezenet"> </ModelElement>
            <ModelElement importNet={this.props.importNet} framework="caffe" id="SENet" displayName="SENet"> </ModelElement>
            <ModelElement importNet={this.props.importNet} framework="keras" id="imdb_cnn_lstm" displayName="IMDB CNN LSTM"> </ModelElement>
            <ModelElement importNet={this.props.importNet} framework="caffe" id="simpleNet" displayName="SimpleNet"> </ModelElement>
          </div>
          <div ref="detection">
            <ModelElement importNet={this.props.importNet} framework="caffe" id="vanilla" displayName="Vanilla CNN"> </ModelElement>
            <ModelElement importNet={this.props.importNet} framework="caffe" id="fcn" displayName="FCN32 Pascal"> </ModelElement>
            <ModelElement importNet={this.props.importNet} framework="caffe" id="yolo_net" displayName="YOLONet"> </ModelElement>
            <ModelElement importNet={this.props.importNet} framework="caffe" id="HED" displayName="HED"> </ModelElement>
          </div>
          <div ref="retrieval">
            <ModelElement importNet={this.props.importNet} framework="caffe" id="siamese_mnist" displayName="MNIST Siamese"> </ModelElement>
            <ModelElement importNet={this.props.importNet} framework="caffe" id="colornet" displayName="Colornet"> </ModelElement>
          </div>
          <div ref="seq2seq">
            <ModelElement importNet={this.props.importNet} framework="keras" id="textGeneration" displayName="Text Generation"> </ModelElement>
            <ModelElement importNet={this.props.importNet} framework="keras" id="seq2seq_lang" displayName="Seq2Seq Translation"> </ModelElement>
            <ModelElement importNet={this.props.importNet} framework="caffe" id="pix2pix" displayName="Pix2Pix"> </ModelElement>
            <ModelElement importNet={this.props.importNet} framework="keras" id="DAE_MNIST" displayName="Denoising Auto-Encoder"> </ModelElement>
          </div>
          <div ref="caption">
            <ModelElement importNet={this.props.importNet} framework="caffe" id="CoCo_Caption" displayName="CoCo Caption"> </ModelElement>
          </div>
          <div ref="segmentation">
            <ModelElement importNet={this.props.importNet} framework="caffe" id="fcn2" displayName="Semantic Segmentation"> </ModelElement>
            <ModelElement importNet={this.props.importNet} framework="keras" id="ZF_UNET_224" displayName="UNET"> </ModelElement>
          </div>
          <div ref="vqa">
            <ModelElement importNet={this.props.importNet} framework="keras" id="VQA" displayName="VQA"> </ModelElement>
            <ModelElement importNet={this.props.importNet} framework="keras" id="VQA2" displayName="VQA2"> </ModelElement>
            <ModelElement importNet={this.props.importNet} framework="caffe" id="mlpVQA" displayName="VQS"> </ModelElement>
          </div>
        </div>
      </div>
    </div>
    );
  }
}

ModelZoo.propTypes = {
  importNet: React.PropTypes.func
};

export default ModelZoo;
