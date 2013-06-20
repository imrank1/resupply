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
		jquery: '//ajax.googleapis.com/ajax/libs/jquery/1/jquery.min',
		underscore: 'ext/underscore',
		backbone: 'ext/backbone',
		templates: '../templates'
	}

});
require(['homePage'], function(HomePage) {
	window.HomePage = new HomePage({ el: '#infoContainer' });
});