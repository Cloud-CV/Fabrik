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
                  <button className="btn btn-primary dropdown-toggle form-control" type="button" id="dropdownMenu1" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">
                    Export
                  </button>
                  <ul className="dropdown-menu pull-right"  aria-labelledby="dropdownMenu1">
                    <li><a href="#" onClick={() => this.props.exportNet('caffe')}>caffe</a></li>
                    <li><a href="#" onClick={() => this.props.exportNet('tensorflow')}>tensorflow</a></li>
                  </ul>
                </div>
              </div>
              <div className="form-group" style={{'float':'right'}}>
                <label htmlFor="inputFile" className="btn btn-primary form-control">
                  Import
                </label>
                <input id="inputFile" type="file" onChange={this.props.importNet}/>
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
