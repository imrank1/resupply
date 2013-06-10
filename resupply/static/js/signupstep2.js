define(['jquery','underscore','backbone'], function($,_,Backbone) {

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
                    debugger;
                    var name = $('#name').val();
                    var e = $('#email').val();
                    var password = $('#password').val();
                    var shippingAddress = $('#shipping-address').val();
                    var shippingAddress2 = $('#shipping-address2').val();
                    var shippingCity = $('#shipping-city').val();
                    var shippingZip = $('#shipping-zipcode').val();
                    var shippingState = $('#shipping-state').val();
                    var phone = $('#shipping-phone').val();
                    $.ajax({
                      url: '/stageCharge',
                      type: 'post',
                      async: true,
                      data: { name: name,email:e,password:password,shippingAddress:shippingAddress,shippingAddress2:shippingAddress2,shippingCity:shippingCity,shippingZip:shippingZip,shippingState:shippingState,shippingPhone:phone,packageType:window.packageType},
                      cache: false,
                      success: function(){

                        window.location= "/finalStep";
                             }   
                        ,
                      error: function(){
                        alert('error');
                        $("#signupFailure").show("slow");
                        }
                    });

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
            // var self = this;
            // var variables = { packageType: window.packageType };
            // $(self.el).template(TEMPLATE_URL + '/templates/billing_include.html', variables);

            //  return this;
        }

})});
