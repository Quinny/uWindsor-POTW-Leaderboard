;(function(angular) {
  angular.module('LeaderBoardApp.factories', []);
  angular.module('LeaderBoardApp.services', []);
  angular.module('LeaderBoardApp.controllers', []);
  angular.module('LeaderBoardApp.directives', []);


  var app = angular.module('LeaderBoardApp', [
      'ngRoute',
      'LeaderBoardApp.factories',
      'LeaderBoardApp.services',
      'LeaderBoardApp.directives',
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
      .otherwise('/');
  }]);

  app.controller('MainCtrl', ['$scope', MainCtrl]);

  function MainCtrl($scope) { }

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

    function UserCollection(rank) {
      var self = this;
      self.rank = rank;
      self.collection = [];
    }

    return {
      build: function(data) {
        return data.map(function(d) {
          return User.build(d.student_id, d.solved);
        }).sort(sortAscending);
      }
    };
  }]);

})(window.angular.module('LeaderBoardApp.factories'));
;(function(app) {
  var host = '';//"http://potw.quinnftw.com";
  var path = "/api/solvers";

  app.factory('LeaderBoardService', ['$http', '$q', LeaderBoardService]);

  function LeaderBoardService($http, $q) {
    self = this;

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

  app.directive('deferCss', ['$parse', '$timeout', directive]);

  function directive($parse, $timeout) {
    return {
      link: function(scope, elem, attrs) {
        var css = $parse(attrs['deferCss'])(scope);
        var time = $parse(attrs['deferCssTime'])(scope) || 1000;
        if (typeof css === 'string' && css.length > 0) {
          $timeout(function() {
            elem.addClass(css);
          }, time);
        }
      }
    }
  }

})(window.angular.module('LeaderBoardApp.directives'));
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
    load();

    function load() {
      getData();
    }

    function getData() {
      LBSvc.getLeaders()
        .then(function success(s) {
          console.log(s);
          $scope.users = Users.build(s.data.data);
        }, function error(err) {
          console.log(err);
          $location.path('/error');
        });
    }
  }

})(window.angular.module('LeaderBoardApp.controllers'));
