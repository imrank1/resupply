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
define(['backbone', 'models/household/HouseholdList'], function(Backbone, HouseholdList) {
	var PricingView = Backbone.View.extend({
		initialize: function() {
			this.collection = new HouseholdList(window.pricingData);
			console.log(this.collection.toJSON());
		}
	});
	return new PricingView();
});
