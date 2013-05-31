require(['ext/jquery', 'ext/underscore', 'ext/backbone', 'homePage', 'template'], function() {
    $(document).ready(function() {
        window.HomePage = new HomePage({ el: $('#infoContainer') });
    });
});