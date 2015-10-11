;(function(angular) {
  angular.module('LeaderBoardApp.factories', []);
  angular.module('LeaderBoardApp.services', []);
  angular.module('LeaderBoardApp.controllers', []);

  var app = angular.module('LeaderBoardApp', [
      'ngRoute',
      'LeaderBoardApp.factories',
      'LeaderBoardApp.services',
      'LeaderBoardApp.controllers'
  ]);

  app.config(['$routeProvider', function($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'leaderBoardTmpl'
      })
      .when('/error', {
        templateUrl: 'errorTmpl'
      })
      .otherwise('/error');
  }]);

  app.controller('MainCtrl', ['$scope', MainCtrl]);

  function MainCtrl($scope) {}

})(window.angular);
;(function(app) {

  function User(id, numSolved) {
    this.name = id;
    this.solved = numSolved;
  }

  app.factory('UserFactory', function() {
    return {
      build: function(id, numSolved) {
        return new User(id, numSolved);
      }
    }
  });

})(window.angular.module('LeaderBoardApp.factories'));
;(function(app) {

  app.factory('UsersFactory', ['UserFactory', function(User) {

    function sortAscending(a, b) {
      if (a.solved > b.solved) {
        return -1;
      }
      if (a.solved < b.solved) {
        return 1;
      }
      return 0;
    }

    return {
      build: function(data) {
        return data.map(function(d) { return User.build(d.student_id, d.solved); }).sort(sortAscending);
      }
    };
  }]);

})(window.angular.module('LeaderBoardApp.factories'));
;(function(app) {
  var host = '';
  var path = "/api/solvers";

  app.factory('LeaderBoardService', ['$http', '$q', LeaderBoardService]);

  function LeaderBoardService($http, $q) {
    return {
      getLeaders: function() {
        var deferred = $q.defer();
        $http({ method: 'GET', url: host + path }).then(deferred.resolve, deferred.reject);

        return deferred.promise;
      }
    }
  }
})(window.angular.module('LeaderBoardApp.services'));
;(function(app) {
  app.controller('ErrorController', ['$scope', '$location', ErrorController]);

  function ErrorController($scope, $location) {
    load();

    function load() {
      $scope.refresh = refresh;
    }

    function refresh() {
      $location.path('/');
    }
  }

})(window.angular.module('LeaderBoardApp.controllers'));
;(function(app) {
  app.controller('LeaderBoardController', ['$scope', '$location', 'LeaderBoardService', 'UsersFactory', LeaderBoardController]);

  function LeaderBoardController($scope, $location, LBSvc, Users) {
    $scope.page = { loading: true };
    load();

    function load() {
      getData();
    }

    function getData() {
      LBSvc.getLeaders()
        .then(function success(s) {
          $scope.page.loading = false;
          $scope.users = Users.build(s.data.data);
        }, function error(err) {
          $scope.page.loading = false;
          $location.path('/error');
        });
    }
  }

})(window.angular.module('LeaderBoardApp.controllers'));
