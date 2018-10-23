var UserProfile = (function() {
  var userId = null;
  var username = null;

  var getUserId = function() {
    return userId;
  };

  var setUserId = function(id) {
    userId = id;
  };

  var getUsername = function() {
    if (username)
      return username;
    return 'Anonymous';
  };

  var setUsername = function(name) {
    username = name;
  };

  return {
    getUserId: getUserId,
    setUserId: setUserId,
    getUsername: getUsername,
    setUsername: setUsername
  }

})();

export default UserProfile;
