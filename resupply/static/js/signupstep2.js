(function() {
    var TEMPLATE_URL = '/static';
    window.SignupStep2 = Backbone.View.extend({
        events: {
            "click #finalSignupButton": "processSignup"
        },

        initialize: function(options) {

        },

        processSignup:function(e){
            self = this;
            e.preventDefault();
            $(".alert-error").hide();
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
            if(password.length <= 5){
                 $("#passwordLengthBad").show();
                return false;
            }

            $.ajax({
            url: '/checkEmail' + '?emailAddress=' + $('#email').val(),
            type: 'GET',
            cache: false,
            statusCode : { 
                200: function(){

        var name = $('#name').val();
        var e = $('#email').val();
        var password = $('#password').val();
        var shippingAddress = $('#shipping-address').val();
        var shippingAddress2 = $('#shipping-address2').val();
        var shippingCity = $('#shipping-city').val();
        var shippingZip = $('#shipping-zipcode').val();
        $.ajax({
          url: '/stageCharge',
          type: 'post',
          data: { name: name,email:e,password:password,shippingAddress:shippingAddress,shippingAddress2:shippingAddress2,shippingCity:shippingCity,shippingZip:shippingZip,packageType:window.packageType},
          cache: false,
          success: function(){
            // $("#billingDetails").hide();
            // $("#packageHeader").hide();
            // $("#signupSuccess").removeAttr("disabled");

            // $("#signupSuccess").toggle();
            window.location.href = "/finalStep";
            // window.spinner.stop();
            // $("#successMessage").show("slow");
            // $(".submit-button").removeAttr("disabled");
            // $("#payment-form").find('input:text, input:password, input:file, select, textarea').val('');
            // $("#payment-form").find('input:radio, input:checkbox').removeAttr('checked').removeAttr('selected');          
        }   
            ,
          error: function(){
            alert('error');
            $("#signupFailure").show("slow");
            //   $("#errorMessage").text()
            // $("#errorMessage").show("slow");
          }
        });






                // StripeCheckout.open({
                //     key:         'pk_07vkx4yqszys5bnTNnHPSAAimkCie',
                //     address:     true,
                //     amount:      price,
                //     name:        'Resupply',
                //     description: 'Subscription',
                //     panelLabel:  'Subscription Per Month',
                //     token:       self.stripeResponseHandler
                // });
                return this;
            },
                500: function(){
                    $("#emailInUse").show("slow");
                    return false;
            }
          }
        });



            return false;
        }

        return this;

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
