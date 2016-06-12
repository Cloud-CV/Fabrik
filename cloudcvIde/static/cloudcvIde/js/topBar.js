import React from 'react'

export default React.createClass({
  render() {
    return <div className="topBar">
    CloudCV IDE 
	<input className="btn btn-success" type="submit" value="Import"/>
    <input className="btn btn-success" type="submit" value="Export"/>
    </div>
  }
})