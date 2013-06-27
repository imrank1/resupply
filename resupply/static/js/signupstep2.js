define(['jquery','underscore','backbone'], function($,_,Backbone) {

    var TEMPLATE_URL = '/static';
    window.SignupStep2 = Backbone.View.extend({
        events: {
            "click #finalSignupButton": "processSignup"
        },

        initialize: function(options) {

        },

        processSignup:function(e){
            debugger;
            self = this;
            e.preventDefault();
            $(".alert-error").hide();
            var missingFields = false;
            var error=false;
            var passwordMatch = true;
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
                Stripe.card.createToken({
                    name:$('.card-name').val(),
                    number: $('.card-number').val(),
                    cvc: $('.card-cvc').val(),
                    exp_month: $('.card-expiry-month').val(),
                    exp_year: $('.card-expiry-year').val(),
                    address_zip: $('.card-zip').val(),   
                    address_city: $('.card-city').val()
                }, self.stripeResponseHandler);    
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


    stripeResponseHandler :function(status,response) {
    if (response.error) {
        $("#payment-errors").text(response.error.message).show();
      } else {
        var token = response['id'];

        var name = $('#name').val();
        var e = $('#email').val();
        var password = $('#password').val();
        var shippingAddress = $('#shipping-address').val();
        var shippingAddress2 = $('#shipping-address2').val();
        var shippingCity = $('#shipping-city').val();
        var shippingZip = $('#shipping-zipcode').val();
        var shippingPhone = $('#shipping-phone').val();
        var shippingState = $('#shipping-state').val();
        $.ajax({
          url: '/charge',
          type: 'post',
          data: { name: name,email:e,password:password,shippingAddress:shippingAddress,shippingAddress2:shippingAddress2,shippingZip:shippingZip,shippingState:shippingState,shippingPhone:shippingPhone,stripeToken:token,packageType:window.packageType},
          cache: false,
          success: function(){
            window.location.href = "/account";
          },
          error: function(){
            $("#signupFailure").show("slow");
          }
        });
        return false;
      }
    },

    render: function() {
        // var self = this;
        // var variables = { packageType: window.packageType };
        // $(self.el).template(TEMPLATE_URL + '/templates/billing_include.html', variables);
            //  return this;
        }

})});
