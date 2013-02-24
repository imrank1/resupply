require(['ext/jquery', 'ext/underscore', 'ext/backbone', 'template', 'account'], function() {
    $(document).ready(function() {
        window.Account = new Account({ el: $('#updateShippingSection') });
    });
});