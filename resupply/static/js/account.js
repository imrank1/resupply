(function() {
    var TEMPLATE_URL = '/static';
    window.Account = Backbone.View.extend({
        events: {
            "click #updateAddress": "updateShippingAddress",
            "click #passwordChangeRequestButton": "requestPasswordChange",
            "click #cancelAccountButton":"showCancelConfirm",
            "click #confirmCancelButton": "cancelAccount"
        },

        initialize: function(options) {

        },
    cancelAccount:function(e){
        e.preventDefault();
         $.ajax({
          url: '/cancelAccount',
          type: 'POST',
          data: { },
          cache: false,
          success: function(){
            $("#successCancel").toggle();
            $('#confirmCancelButton').addClass('disabled');
            setTimeout(function() {
                window.location.href = "/index";
            }, 10000);
            return;
        },
        error: function(){
             $("#failureCancel").toggle();
        }
        });
    },

    showCancelConfirm:function(e){
        e.preventDefault();
        $('#cancelAccountConfirm').toggle();
    },
    showPasswordRestConfirm:function(e){
      debugger;
        $('#passwordChangeConfirm').modal()
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

      requestPasswordChange:function(e){
        debugger;
        self = this;
        e.preventDefault();
        $.ajax({
          url: '/requestPasswordChange',
          type: 'POST',
          data: { },
          cache:false,
          success: function(){
            $("#passwordChangeEmailSent").toggle();
            return;
        },
        error: function(){
            $("#passwordChangeRequestFailure").show("slow");
        }
        });
        return false;
      },

    render: function() {
            // var self = this;
            // var variables = { packageType: window.packageType };
            // $(self.el).template(TEMPLATE_URL + '/templates/billing_include.html', variables);

            return this;
        }
    });
}());
