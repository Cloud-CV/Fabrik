import React from 'react';

function TopBar({ exportNet }) {
  return (
    <div className="topBar">
      CloudCV IDE
      <input
        className="btn btn-success"
        type="submit"
        value="Import"
      />
      <input
        className="btn btn-success"
        onClick={exportNet}
        type="submit"
        value="Export"
      />
    </div>
  );
}

TopBar.propTypes = {
  exportNet: React.PropTypes.func,
};

export default TopBar;
