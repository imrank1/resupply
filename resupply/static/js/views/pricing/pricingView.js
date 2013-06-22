require.config({
	baseUrl: 'static/js',
	shim: {
		underscore: {
			exports: '_',
			deps: ['text']
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
		templates: '../templates',
		text: 'lib/require_text'
	}

});
define(['backbone', 'models/household/HouseholdList', 'text!views/pricing/pricingTmpl.html'], function(Backbone, HouseholdList, tmpl) {
	var PricingView = Backbone.View.extend({
		initialize: function() {
			// note: currentPackage key only set if user is logged in
			this.model = new Backbone.Model(window.resupply);
			this.householdList = new HouseholdList(window.pricingData);

			console.log(this.model.toJSON());
			console.log(this.householdList.toJSON());
			console.log(tmpl);
		},

		render: function() {
		}
	});
	return new PricingView();
});
