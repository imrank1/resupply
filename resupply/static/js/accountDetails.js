require(['ext/jquery', 'ext/underscore', 'ext/backbone', 'template', 'account','bootstrap'], function() {
    $(document).ready(function() {
        window.Account = new Account({ el: $('#updateShippingSection') });
    });
});