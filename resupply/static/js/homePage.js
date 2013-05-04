(function() {
    var TEMPLATE_URL = '/static';
    window.HomePage = Backbone.View.extend({
        events: {
            "click #getStarted": "processGetStarted"
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
  

            $.ajax({
            url: '/getStarted',
            type: 'POST',
            data:{zipCode:zipCode,numFamily:numFamily},
            cache: false,
            statusCode : { 
                200: function(){
                window.location = '/pricing';
                return this;
            },
                500: function(){
                    $("#cantShipThere").show("slow");
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
