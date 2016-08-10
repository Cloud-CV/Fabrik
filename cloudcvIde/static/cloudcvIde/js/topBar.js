import React from 'react';

class TopBar extends React.Component {
  render() {
    return (
      <div className="topBar">
        <div className="row">
          <div className="col-md-7 topBarHead" >
            CloudCV IDE
          </div>
          <div className="col-md-5" >
            <div className="form-inline">
              <div className="form-group" style={{'float':'right'}}>
                <div className="dropdown">
                  <button className="btn btn-primary dropdown-toggle form-control" data-toggle="dropdown">
                    Export
                  </button>
                  <ul className="dropdown-menu pull-right">
                    <li><a href="#" onClick={() => this.props.exportNet('caffe')}>caffe</a></li>
                    <li><a href="#" onClick={() => this.props.exportNet('tensorflow')}>tensorflow</a></li>
                  </ul>
                </div>
              </div>
              <div className="form-group" style={{'float':'right'}}>
                <div className="dropdown">
                  <button className="btn btn-primary dropdown-toggle form-control" data-toggle="dropdown">
                    Import
                  </button>
                  <ul className="dropdown-menu pull-right">
                    <li>
                        <a>
                        <label htmlFor="inputFilecaffe">caffe</label>
                        <input id="inputFilecaffe" type="file" onChange={() => this.props.importNet('caffe')}/>
                        </a>
                    </li>
                    <li>
                        <a>
                        <label htmlFor="inputFiletensorflow">tensorflow</label>
                        <input id="inputFiletensorflow" type="file" onChange={() => this.props.importNet('tensorflow')}/>
                        </a>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

TopBar.propTypes = {
  exportNet: React.PropTypes.func,
  importNet: React.PropTypes.func,
};

export default TopBar;
