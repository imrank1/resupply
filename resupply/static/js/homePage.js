(function() {
    var TEMPLATE_URL = '/static';
    window.HomePage = Backbone.View.extend({
        events: {
            "click #getStarted": "processGetStarted",
            "click #ontoPricing": "processGetStarted",
            "click #subscribe": "addToSubscribe"
        },

        initialize: function(options) {

        },

        processGetStarted:function(e){
            self = this;
            e.preventDefault();
            var missingFields = false;
            var error=false;
            $(".requiredStuff").each(function(){
                if($(this).val()==""){
                    $(this).addClass("errorState");
                    missingFields=true;
                }
            });

            if(missingFields==true){
                $("#getStartedErrorMessage").show();
            }else {

            var zipCode = $("#zipCode").val();
            var numFamily = $("#numFamily").val();
            var gender = $('input:radio[name=gender]:checked').val();
  

            $.ajax({
            url: '/getStarted',
            type: 'POST',
            data:{zipCode:zipCode,numFamily:numFamily,gender:gender},
            cache: false,
            statusCode : { 
                200: function(){
                window.location = '/pricing';
                return this;
            },
                500: function(){
                    $("#cantShipThere").show("slow");
                    $("#subscribeBox").show("slow");
                    return false;
            }
          }
        });



            return false;
        }

        return this;

        },
        addToSubscribe:function(e){
            debugger;
            self = this;
            e.preventDefault();
            var missingFields = false;
            var error=false;
            $(".requiredSforSubscribe").each(function(){
                if($(this).val()==""){
                    $(this).addClass("errorState");
                    missingFields=true;
                }
            });

            if(missingFields==true){
                $("#subscribeErrorMessage").show();
            }else {

            var email = $("#emailAddressSubscribe").val();
           

            $.ajax({
            url: '/addToSubscribe',
            type: 'POST',
            data:{email:email,},
            cache: false,
            statusCode : { 
                200: function(){
                $("#subscribeSuccess").show();
                
                return this;
            },
                500: function(){
                    $("#subscribeError").show("slow");
                    return false;
            }
          }
        });



            return false;
        }

        return this;

        },
        isNumber:function(n) {
            return !isNaN(parseFloat(n)) && isFinite(n);
        }
    });
}());
