var myApp = angular.module('myApp', []);

myApp.directive('fileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;

            element.bind('change', function(){
                scope.$apply(function(){
                    modelSetter(scope, element[0].files[0]);
                });
            });
        }
    };
}]);

myApp.service('fileUpload', ['$http', function ($http) {

}]);

myApp.controller('myCtrl', ['$scope','fileUpload', '$http',function($scope, fileUpload,$http)
{
    $scope.out = "";
    $scope.uploadUrl = ""
    $scope.hidebinoy = true;
    $scope.hidekaushik = true;
    $scope.hideharshit = true;

    $scope.remarks =
    {
        col1 : 0,
        col2 : false,
        col3 : "N.A",
        col4 : "",
        col5 : "",
        col6 : "",
        col7 : "",
        col8 : "",
        col9 : "",
        col10 : ""
    };

    $scope.refresher = function()
    {
        $scope.out = "";
        $scope.uploadUrl = ""
        $scope.hidebinoy = true;
        $scope.hidekaushik = true;
        $scope.hideharshit = true;

        $scope.remarks =
            {
                col1 : 0,
                col2 : false,
                col3 : "N.A",
                col4 : "",
                col5 : "",
                col6 : "",
                col7 : "",
                col8 : "",
                col9 : "",
                    col10 : ""
            };
        window.location.href = "http://ec2-52-10-224-75.us-west-2.compute.amazonaws.com/index.html"
    };

    $scope.logout = function(){
        delete $sessionStorage;
        console.log("session cleared");
        window.location.href = "http://ec2-52-10-224-75.us-west-2.compute.amazonaws.com/login.html";
    }

    $scope.submitForm = function()
    {
        if($scope.tenanturl == "Binoy")
            {
                $scope.uploadUrl = "http://testLB-1695287167.us-west-2.elb.amazonaws.com:80";
            }
        if($scope.tenanturl == "Harshit")
            {
               $scope.uploadUrl = "http://testLB-1695287167.us-west-2.elb.amazonaws.com:82";
            }
        if($scope.tenanturl == "Kaushik")
            {
                $scope.uploadUrl = "http://testLB-1695287167.us-west-2.elb.amazonaws.com:81";
            }
        if($scope.tenanturl== "Apoorva")
            {
                $scope.uploadUrl = "http://testLB-1695287167.us-west-2.elb.amazonaws.com:83";
            }
    };

    console.log($scope.uploadUrl );

    $scope.uploadFile = function()
    {
        var file = $scope.myFile;
        console.log('file is ' );
        console.dir(file);
        console.log($scope.uploadUrl)
         uploadFileToUrl(file, $scope.uploadUrl);
    };

    $scope.viewFile = function()
    {
        $scope.hidden = false
        if($scope.uploadUrl == "http://testLB-1695287167.us-west-2.elb.amazonaws.com:80")
        {
            $scope.hidebinoy = false;
        }
        if($scope.uploadUrl == "http://testLB-1695287167.us-west-2.elb.amazonaws.com:81")
        {
            $scope.hidekaushik = false;
        }
        if($scope.uploadUrl == "http://testLB-1695287167.us-west-2.elb.amazonaws.com:82")
        {
            $scope.hideharshit = false;
        }
        if($scope.uploadUrl == "http://testLB-1695287167.us-west-2.elb.amazonaws.com:83")
        {
            $scope.hideapoorva = false;
        }
        getfile($scope.out);

    };

    $scope.submitFeedback = function()
    {
        console.log($scope.remarks);
        $http.post($scope.uploadUrl + "/grade",$scope.remarks).success(function(responseData)
        {
            console.log(responseData);
        })
        .error(function()
        {
            console.log("request failed");
        });
    };

    function uploadFileToUrl(file, uploadUrl)
    {
        var fd = new FormData();
        fd.append('file', file);
        $http.post(uploadUrl, fd,
        {
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined}
        })
        .success(function(responseData)
        {
            $scope.out= responseData
            $scope.switch = false
        })
        .error(function()
        {
        });
    }

    function getfile(imgname)
    {
        var imagelink = $scope.uploadUrl + "/static/" + imgname;
        $http({
        method : "GET",
        url : $scope.uploadUrl + "/view/" + imgname
    }).then(function mySuccess(response)
    {
        $scope.img = response.data;
        $scope.imglink = imagelink
    }, function myError(response)
    {
        $scope.img = "image unavailable";
    });
    }

}]);

