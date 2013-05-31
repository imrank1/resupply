require(['ext/jquery', 'ext/underscore', 'ext/backbone', 'template', 'password'], function() {
    $(document).ready(function() {
    	debugger;
        window.Password = new Password({ el: $('#passwordSettings') });
    });
});