import React from 'react';

class Login extends React.Component {
  constructor(props) {
    super(props);
    this.checkLogin = this.checkLogin.bind(this);
    this.logoutUser = this.logoutUser.bind(this);
  }
  componentWillMount() {
    this.setState({ loginState: false });
    this.checkLogin();
  }
  checkLogin() {
    $.ajax({
      url: '/backendAPI/checkLogin',
      type: 'GET',
      processData: false,  // tell jQuery not to process the data
      contentType: false,
      success: function (response) {
        if (response.result) {
          this.setState({ loginState: response.result });
          this.props.setUserId(response.user_id);
          this.props.setUserName(response.username);
        }
      }.bind(this),
      error: function () {
        this.setState({ loginState: false });
      }.bind(this)
    });
  }
  logoutUser() {
    $.ajax({
      url: '/accounts/logout',
      type: 'GET',
      processData: false,  // tell jQuery not to process the data
      contentType: false,
      success: function (response) {
        if (response) {
          this.setState({ loginState: false });
          this.props.setUserId(null);
          this.props.setUserName(null);
        }
      }.bind(this),
      error: function () {
        this.setState({ loginState: true });
        this.addError("Error occurred while logging out");
      }.bind(this)
    });
  }
  render() {
    if(this.state.loginState) {
      return (
        <div>
          <a className="btn btn-block extra-buttons text-left" onClick={ () => this.logoutUser() }>Logout</a>
        </div>
      )
    }
    else {
      return (
        <div className="row">
          <div className="col-md-6">
            <a className="btn btn-block btn-social btn-github" onClick={() => window.location="/accounts/github/login"} style={{width: '105px'}}>
              <span className="fa fa-github"></span>Github
            </a>
          </div>

          <div className="col-md-5">
            <a className="btn btn-block btn-social btn-google" onClick={() => window.location="/accounts/google/login"}  style={{width: '105px'}}>
              <span className="fa fa-google"></span>Google
            </a>
          </div>
        </div>
      )
    }
  }
}

Login.propTypes = {
  setUserId: React.PropTypes.func,
  setUserName: React.PropTypes.func
};

export default Login;
