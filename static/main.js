(function () {
    'use strict';
  
    angular.module('gfmMetricsApp', [])
  
    .controller('gfmMetricsController', ['$scope', '$log', '$http', '$timeout',
      function($scope, $log, $http, $timeout) {

        $scope.submitButtonText = "Submit";
        $scope.loading = false;
        $scope.urlerror = false;

        $scope.getResults = function() {

          var userInput = $scope.url;

          $http.post('/start', {"url": userInput})
            .success(function(results) {
                $log.log(results);
                getDonationsData(results);
                $scope.submitButtonText = "Loading...";
                $scope.loading = true;
                $scope.urlerror = false;
                $scope.responseData = null;
                $scope.errorsData = null;
            })
            .error(function(error) {
                $log.log(error);
            });

        };

        function getDonationsData(jobID) {

            var timeout = "";

            var poller = function() {
            // fire another request
            $http.get('/results/'+jobID)
                .success(function(data, status, headers, config) {
                if(status === 202) {
                    $log.log(data, status);
                } else if (status === 200){
                    $log.log(data[1]);
                    if (data[0] == "err"){
                      $scope.urlerror = true
                      $scope.loading = false;
                      $scope.responseData = data[1];                    
                      $scope.submitButtonText = "Submit";  
                    }
                    else {
                      $scope.responseData = resultsOrganizer(data[1])
                      $scope.loading = false;
                      $scope.submitButtonText = "Submit";
                    }
 
                    $timeout.cancel(timeout);
                    return false;
                } 
                // continue to call the poller() function every 2 seconds
                // until the timeout is cancelled
                timeout = $timeout(poller, 2000);
                })
                .error(function(error) {
                    $log.log(error);
                    $scope.urlerror = true;
                    $scope.loading = false;
                    $scope.submitButtonText = "Submit";
                  });
            };

            function resultsOrganizer(input) {
              var dataResponse = {
                numDonors: input[0][1],
                numDonations: input[1][1],
                //listNonnonymous: input[2],
                listDonations: input[3][1],
                //listAnonymous: input[4],
                listComplete: input[5][1],
                bigDonors50: input[6][1],
                bigDonors25: input[7][1],
                bigDonors20: input[8][1],
                bigDonors10: input[9][1],
                bigDonors05: input[10][1],
                bigDonors03: input[11][1],
                bigDonors02: input[12][1],
                bigDonors01: input[13][1]
              };

              var array = dataResponse.listDonations;

              dataResponse['amtTotal'] = array.reduce((s,c) => (s + c), 0);
  
              dataResponse['amtMax'] = Math.max(...array);

              dataResponse['amtMean'] = Math.floor(array.reduce((acc, val) => (acc + val), 0) / array.length);

              var medianArray = array.sort();
              var mid = medianArray.length / 2;
              dataResponse['amtMedian'] = mid % 1 ? medianArray[mid - 0.5] : (medianArray[mid - 1] + medianArray[mid]) / 2;

              return dataResponse;
            };
            poller();
        };
      }
    ])

    .directive('wordCountChart', ['$parse', function ($parse) {
        return {
          restrict: 'E',
          replace: true,
          template: '<div id="chart"></div>',
          link: function (scope) {
            scope.$watch('wordcounts', function() {
                d3.select('#chart').selectAll('*').remove();
                var data = scope.wordcounts;
                for (var word in data) {
                  var key = data[word][0];
                  var value = data[word][1];
                  d3.select('#chart')
                    .append('div')
                    .selectAll('div')
                    .data(word[0])
                    .enter()
                    .append('div')
                    .style('width', function() {
                        return (value * 3) + 'px';
                    })
                    .text(function(d) {
                        return key;
                    });
                }
            }, true);
          }          
         };
      }]);
  }());