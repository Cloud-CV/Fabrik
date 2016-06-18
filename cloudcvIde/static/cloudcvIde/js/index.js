import React from 'react';
import { render } from 'react-dom';
import { Router, Route, hashHistory } from 'react-router';
import App from './app.js';
import '../css/style.css';
import 'bootstrap/dist/css/bootstrap.min.css';

render(
  <Router history={hashHistory}>
    <Route path="/" component={App} />
  </Router>, document.getElementById('app')
);
