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
require(['homePage'], function() {
    $(document).ready(function() {
        window.HomePage = new HomePage({ el: $('#infoContainer') });
    });
});