(function() {
    var TEMPLATE_URL = '/static';
    window.Signup = Backbone.View.extend({
        events: {
            "click #finalSignupButton": "processSignup"
        },

        initialize: function(options) {

        },

        processSignup:function(e){
            e.preventDefault();
            var missingFields = false;
            var error=false;
            var passwordMatch = true;
            var price = this.getPackagePrice();
            $(".requiredStuff").each(function(){
                if($(this).val()==""){
                    $(this).addClass("errorState");
                    missingFields=true;
                }
            });

            if(missingFields==true){
                $("#signupErrorMessage").show();
            }else {

            var password = $("#password").val();
            var passwordConfirm = $("#passwordConfirm").val();
            if(!error){
                if(password != passwordConfirm){
                    passwordMatch = false;
                }
            }
            if(!passwordMatch){
                $("#passwordMismatchError").show();
                return false;
            }


            StripeCheckout.open({
                key:         'pk_07vkx4yqszys5bnTNnHPSAAimkCie',
                address:     true,
                amount:      price,
                name:        'Resupply',
                description: 'Subscription',
                panelLabel:  'Subscription Per Month',
                token:       this.stripeResponseHandler
            });

                return false;
            }

            return this;

        },

    stripeResponseHandler :function(response) {
        debugger;
    if (response.error) {
        alert('somthing went wrong');
        // window.spinner.stop();

        // // show the errors on the form
        // $("#paymentErrorMessage").show("slow");
        // $(".submit-button").removeAttr("disabled");
      } else {
        var form$ = $("#payment-form");
        var token = response['id'];

        var name = $('#name').val();
        var e = $('#email').val();
        var password = $('#password').val();
        var shippingAddress = $('#shipping-address').val();
        var shippingAddress2 = $('#shipping-address2').val();
        var shippingCity = $('#shipping-city').val();
        var shippingZip = $('#shipping-zipcode').val();
        $.ajax({
          url: '/charge',
          type: 'post',
          data: { name: name,email:e,password:password,shippingAddress:shippingAddress,shippingAddress2:shippingAddress2,shippingCity:shippingCity,shippingZip:shippingZip,stripeToken:token,packageType:window.packageType},
          cache: false,
          success: function(){
            alert('awesome we got it done')
            // window.spinner.stop();
            // $("#successMessage").show("slow");
            // $(".submit-button").removeAttr("disabled");
            // $("#payment-form").find('input:text, input:password, input:file, select, textarea').val('');
            // $("#payment-form").find('input:radio, input:checkbox').removeAttr('checked').removeAttr('selected');          
        }   
            ,
          error: function(){
            alert('error');
            //   $("#errorMessage").text()
            // $("#errorMessage").show("slow");
          }
        });
        // $(".submit-button").removeAttr("disabled");
        return false;
      }
    },

        getPackagePrice:function(){
            var packagePrice; 
            switch(window.packageType)
            {
                case "basic":
                    packagePrice = 17*100;
                    break;
                case "basicPlus":
                    packagePrice = 20*100;
                    break;
                case "premium":
                    packagePrice =  25*100;
                    break;
                case "premiumPlus":
                    packagePrice =  28*100;
                    break;
                default:
                    packagePrice =  17*100;
            }
            return packagePrice;
        },

        render: function() {
            var self = this;
            var variables = { packageType: window.packageType };
            $(self.el).template(TEMPLATE_URL + '/templates/billing_include.html', variables);

            return this;
        }
    });
}());
