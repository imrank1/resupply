define(['jquery','underscore','backbone'], function($,_,Backbone) {
    var TEMPLATE_URL = '/static';
    window.ContactForm = Backbone.View.extend({
        events: {
            "click #contact-submit": "submitQuestion"
        },

        initialize: function(options) {

        },

        submitQuestion:function(e){
            e.preventDefault();
            $('.alert-error').hide();
            self = this;
            $(".alert-error").hide();
            var missingFields = false;
            var error=false;
            $(".requiredStuff").each(function(){
                if($(this).val()==""){
                    $(this).addClass("errorState");
                    missingFields=true;
                }
            });

            if(missingFields==true){
                $("#signupErrorMessage").show();
            }else {
            var name = $("#name").val();
            var email = $("#email").val();
            var message = $("#message").val();
           
            $.ajax({
            url: '/contact-submit',
            type: 'post',
            data: { name: name,email:email,message:message},
            cache: false,
            success: function(){
                $("#submitted").show("slow");
            },
            error: function(){
                $("#error").show("slow");
            } 
        });



            return false;
        }

        return this;

        }
})});
   