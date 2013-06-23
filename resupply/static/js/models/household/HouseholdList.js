define(['backbone', 'models/household/Household'], function(Backbone, Household) {
	return Backbone.Collection.extend({
		model: Household
	});
});
