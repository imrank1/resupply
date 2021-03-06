define(['jquery','underscore','backbone'], function($,_,Backbone) {
	var TEMPLATE_URL = '/static';
	var HomePage = Backbone.View.extend({
		events: {
			"click #getStarted": "processGetStarted",
			"click #ontoPricing": "processGetStarted",
			"click #ontoPricingUpgrade": "processGetStartedUpgrade",
			"click #subscribe": "addToSubscribe"
		},

		initialize: function(options) {

		},

		processGetStarted:function(e){
			var self = this;
			e.preventDefault();
			var missingFields = false;
			var error=false;
			$(".requiredStuff").each(function(){
				var $input = $(this);
				if(!$input.val()){
					$input.addClass("errorState");
					missingFields = true;
				}
			});

			if(missingFields) {
				$("#getStartedErrorMessage").show();
			} else {
				var zipCode = $("#zipCode").val();
				var numFamily = $("#numFamily").val();
				var gender = $('input:radio[name=gender]:checked').val();

				$.ajax({
					url: '/getStarted',
					type: 'POST',
					data:{zipCode:zipCode,numFamily:numFamily,gender:gender},
					cache: false,
					statusCode : {
						200: function(){
							window.location = '/pricing';
							return this;
						},
						500: function(){
							$("#cantShipThere").show("slow");
							$("#subscribeBox").show("slow");
							return false;
						}
					}
				});
				return false;
			}

			return this;
		},
		processGetStartedUpgrade:function(e){
			var self = this;
			e.preventDefault();
			var missingFields = false;
			var error=false;
			$(".requiredStuff").each(function(){
				var $input = $(this);
				if(!$input.val()){
					$input.addClass("errorState");
					missingFields=true;
				}
			});

			if(missingFields){
				$("#getStartedErrorMessage").show();
			}else {

				var numFamily = $("#numFamily").val();

				$.ajax({
					url: '/getStartedUpgrade',
					type: 'POST',
					data:{numFamily:numFamily},
					cache: false,
					statusCode : {
						200: function(){
							window.location = '/pricing';
							return this;
						},
						500: function(){
							$("#subscribeBox").show("slow");
							return false;
						}

					}
				});

				return false;
			}

			return this;

		},
		addToSubscribe:function(e){
			var self = this;
			e.preventDefault();
			var missingFields = false;
			var error=false;
			$(".requiredSforSubscribe").each(function(){
				var $input = $(this);
				if(!$input.val()){
					$input.addClass("errorState");
					missingFields=true;
				}
			});

			if(missingFields){
				$("#subscribeErrorMessage").show();
			}else {

				var email = $("#emailAddressSubscribe").val();


				$.ajax({
					url: '/addToSubscribe',
					type: 'POST',
					data:{email:email,},
					cache: false,
					statusCode : {
						200: function(){
							$("#subscribeSuccess").show();
							return this;
						},
						500: function(){
							$("#subscribeError").show("slow");
							return false;
						}
					}
				});
				return false;
			}

			return this;

		},
		isNumber:function(n) {
			return !isNaN(parseFloat(n)) && isFinite(n);
		}
	});
	return HomePage;
});
