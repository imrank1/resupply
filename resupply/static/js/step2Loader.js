require(['ext/jquery', 'ext/underscore', 'ext/backbone', 'ext/checkout', 'template','signupstep2'], function() {
    $(document).ready(function() {
        window.App = new SignupStep2({ el: $('#billing_container') });
        window.App.render();
    });
});