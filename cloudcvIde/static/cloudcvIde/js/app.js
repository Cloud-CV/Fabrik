import React from 'react'
import TopBar from './topBar'
import Content from './content'

export default React.createClass({
  render() {
    return  <div className="app">
    		<TopBar></TopBar>
    		<Content ></Content>
    		</div>
  }
})