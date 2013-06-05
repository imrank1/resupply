require.config({
	baseUrl: 'static/js',
  shim: {
    underscore: {
      exports: '_'
    },
    backbone: {
      deps: ['underscore', 'jquery'],
      exports: 'Backbone'
    }
  },
  paths: {
    jquery: 'ext/jquery',
    underscore: 'ext/underscore',
    backbone: 'ext/backbone',
    templates: '../templates'
  }

});


require(['signupstep2'], function() {
    $(document).ready(function() {
        window.App = new SignupStep2({ el: $('#billing_container') });
        window.App.render();
    });
});