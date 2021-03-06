define(['jquery','underscore','backbone'], function($,_,Backbone) {
    var TEMPLATE_URL = '/static';
    window.Password = Backbone.View.extend({
        events: {
            "click #submitPasswordButton": "updatePassword"
        },

        initialize: function(options) {

        },


    updatePassword :function(e) {
        self = this;
        e.preventDefault();
        var newPassword = $('#password1').val();
        var password2 = $('#password2').val();
        var linkRef = $('#linkRef').val();
        
        $.ajax({
          url: '/handlePasswordChange',
          type: 'POST',
          data: { password: newPassword,linkRef:linkRef},
          cache: false,
          success: function(){
            window.location.href = "/signin";
            return;
        },
        error: function(){
            alert('error changing password!');
        }
        });
        return false;
      },

    render: function() {
            // var self = this;
            // var variables = { packageType: window.packageType };
            // $(self.el).template(TEMPLATE_URL + '/templates/billing_include.html', variables);

            // return this;
        }
})});
