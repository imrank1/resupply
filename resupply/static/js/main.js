require(['ext/jquery', 'ext/underscore', 'ext/backbone', 'ext/checkout', 'template','signupCustom'], function() {
    $(document).ready(function() {
        window.App = new Signup({ el: $('#billing_container') });
        window.App.render();
    });
});