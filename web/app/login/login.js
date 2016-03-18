'use strict';

angular.module('myApp.login', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/login', {
    templateUrl: 'login/login.html',
    controller: 'LoginCtrl'
  });
}])

.controller('LoginCtrl', ['$scope', function($scope) {

    $scope.token = false;
    $scope.vault = {};

    $scope.toggleLogin = function(token){
        $scope.token = token;
    };

    $scope.doLogin = function(){

    };


}])

 .service('VaultService', ['$http',  function($http){

        this.login = function(vault) {
            $http.get(vault.host + 'POST /sys/capabilities')
                .success(function(data) {
                    onSuccess(data)
                }).error(function(data){
                    onError(data)
                });
        };

    }]);


