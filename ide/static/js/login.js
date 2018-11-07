import React from 'react';

class Login extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isOpenLoginPanel: false
    }
    this.tryLogin = this.tryLogin.bind(this);
    this.logoutUser = this.logoutUser.bind(this);
  }
  componentWillMount() {
    this.setState({ loginState: false });
  }
  componentDidMount() {
    this.tryLogin(false);
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
    this.setState({ isOpenLoginPanel: false });
  }
  openLoginPanel() {
    this.setState({
      isOpenLoginPanel: true
    });
  }
  closeLoginPanel() {
    this.setState({
      isOpenLoginPanel: false
    });
  }
  tryLogin(showNotification) {
    let username = null;
    let password = null;

    if (this.state.isOpenLoginPanel) {
      username = $('#login-input')[0].value;
      password = $('#password-input')[0].value;
    }

    $.ajax({
      url: '/backendAPI/checkLogin',
      type: 'GET',
      contentType: false,
      data: {
        username: username,
        password: password,
        isOAuth: (!showNotification)
      },
      success: function (response) {
        if (response.result) {
          this.setState({ loginState: response.result });
          this.props.setUserId(response.user_id);
          this.props.setUserName(response.username);

          if (showNotification) {
            $('#successful-login-notification')[0].style.display = 'block';
            $('#successful-login-notification-message')[0].innerHTML = 'Welcome, ' + username + '!';

            setTimeout(() => {
              let elem = $('#successful-login-notification')[0];
              if (elem) {
                elem.style.display = 'none';
              }
            }, 3000);
          }
        }
        else {
          if (showNotification) {
            $('#login-error-message-text')[0].innerHTML = response.error; 
            $('#login-error-message')[0].style.display = 'block'; 
          }
        }
      }.bind(this),
      error: function () {
        this.setState({ loginState: false });
      }.bind(this)
    });
  }
  render() {
    let loginPanel = null;

    if (this.state.isOpenLoginPanel) {
      loginPanel = (
        <div id="login-prepanel" className="login-prepanel-enabled" onClick={
              (e) => {
                if (e.target.id == "login-prepanel" || e.target.id == "login-panel-close") {
                  this.closeLoginPanel();
                }
              }
            }>
            <div className="login-panel">
              <i className="material-icons" id="login-panel-close">close</i>
              <div className="login-logo">
                <a href="http://fabrik.cloudcv.org">
                  <img src="/static/img/fabrik_t.png" className="img-responsive" alt="logo" id="login-logo"></img>
                </a>
              </div>
              <div className="login-panel-main">
                <h5 className="sidebar-heading">
                  LOGIN
                  <div className="login-invalid">- invalid</div>
                </h5>
                <h5 className="sidebar-heading">
                  <input placeholder="login" autoCorrect="off" id="login-input"></input>
                </h5>
                <h5 className="sidebar-heading">
                  PASSWORD
                  <div className="login-invalid">- invalid</div>
                </h5>
                <h5 className="sidebar-heading">
                  <input type="password" placeholder="password" id="password-input"></input>
                </h5>

                <div id="login-error-message">
                  <i className="material-icons">close</i>
                  <div id="login-error-message-text"></div>
                </div>

                <h5 className="sidebar-heading login-prebtn">
                  <div className="col-md-6 login-button" id="login-button">
                    <a className="btn btn-block btn-social" onClick={ () => this.tryLogin(true) } style={{width: '105px'}}>
                      <span className="fa fa-sign-in"></span>Login
                    </a>
                  </div>
                </h5>

                <h5 className="sidebar-heading login-prebtn">
                  <div className="col-md-5 login-button">
                    <a className="btn btn-block btn-social" onClick={() => window.location="/accounts/google/login"}  style={{width: '105px'}}>
                      <span className="fa fa-user-plus"></span>Sign up
                    </a>
                  </div>
                </h5>

                <h5 className="sidebar-heading extra-login">
                  OTHER
                </h5>

                <h5 className="sidebar-heading login-prebtn">
                  <div className="col-md-6">
                    <a className="btn btn-block btn-social btn-github" onClick={
                        () => window.location="/accounts/github/login"
                      } style={{width: '105px'}}>
                      <span className="fa fa-github"></span>Github
                    </a>
                  </div>
                </h5>

                <h5 className="sidebar-heading login-prebtn">
                  <div className="col-md-5">
                    <a className="btn btn-block btn-social btn-google" onClick={
                        () => window.location="/accounts/google/login"
                      }  style={{width: '105px'}}>
                      <span className="fa fa-google"></span>Google
                    </a>
                  </div>
                </h5>

              </div>
            </div> 
          </div>);
    }

    if(this.state.loginState) {
      return (
        <div>
          <h5 className="sidebar-heading" id="sidebar-login-button" onClick={
            () => {
              this.logoutUser();
          }}>
          <div>LOGOUT</div>
          </h5>
          <div id="successful-login-notification">
            <i className="material-icons">done</i>
            <div id="successful-login-notification-message"></div>
          </div>
        </div>
      )
    }
    else {
      return (
        <div>
          <h5 className="sidebar-heading" id="sidebar-login-button" onClick={
            () => {
              this.openLoginPanel();
            }}>
            <div>LOGIN</div>
          </h5>
          {loginPanel}
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
