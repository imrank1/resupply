(function() {
    var TEMPLATE_URL = '/static';
    window.Account = Backbone.View.extend({
        events: {
            "click #updateAddress": "updateShippingAddress"
        },

        initialize: function(options) {

        },


    updateShippingAddress :function(e) {
        self = this;
        e.preventDefault();
        var name = $('#name').val();
        var password = $('#password').val();
        var shippingAddress = $('#shippingAddress').val();
        var shippingAddress2 = $('#shippingAddress2').val();
        var shippingCity = $('#shippingCity').val();
        var shippingZip = $('#shippingZip').val();
        $.ajax({
          url: '/updateShippingAddress',
          type: 'POST',
          data: { shippingAddress: shippingAddress,shippingAddress2:shippingAddress2,shippingCity:shippingCity,shippingZip:shippingZip},
          cache: false,
          success: function(){
            $("#successShippingAddressChange").toggle();
            return;
        },
        error: function(){
            $("#updateBillingFailure").show("slow");
        }
        });
        return false;
      },

    render: function() {
            var self = this;
            var variables = { packageType: window.packageType };
            $(self.el).template(TEMPLATE_URL + '/templates/billing_include.html', variables);

            return this;
        }
    });
}());
