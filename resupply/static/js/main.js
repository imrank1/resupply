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
    templates: '../templates',
  }

});
require(['signupCustom'], function() {
    $(document).ready(function() {
        window.App = new Signup({ el: $('#billing_container') });
        window.App.render();
    });
});