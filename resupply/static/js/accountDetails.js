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

require(['account'], function() {
    $(document).ready(function() {
        window.Account = new Account({ el: $('#updateShippingSection') });
    });
});