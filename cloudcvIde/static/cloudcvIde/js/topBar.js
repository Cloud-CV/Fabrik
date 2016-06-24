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
              <div className="form-group">
                <input id="inputFile" type="file" />
              </div>
              <div className="form-group">
                <input
                  className="btn btn-success form-control"
                  type="submit"
                  value="Import"
                  onClick={this.props.importNet}
                />
              </div>
              <div className="form-group">
                <input
                  className="btn btn-success form-control"
                  onClick={this.props.exportNet}
                  type="submit"
                  value="Export"
                />
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
