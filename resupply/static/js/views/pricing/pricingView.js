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
        el: '.resupply-pricing-container',

        events: {
            'keypress #zipCode': 'zipPress',
            'click #nextStep' : 'setZip',
            'change .household': 'householdChange',
            'click #subscribe' : 'addToSubscribe',
            'click #backToInfo' : 'backtoInfo'
        },

        zipPress: function(e) {
            if(e.keyCode === 13) this.setZip();
        },

        setZip: function() {
            var zip = this.$zip.val();
            if(!/^\d{5}(-\d{4})?$/.test(zip)) return this.$alert.show().html('Invalid zipcode');
            if(parseInt(zip.substr(0,1),10) > 2) {
                $("#cantShipThere").show("slow");
                $("#subscribeBox").show("slow");
                return;
            } 
            this.$alert.hide();
            this.$('.resupply-hero').slideUp();
            this.$chartContainer.slideDown();

            // makes request to store session zipcode
            $.ajax({
                url: '/getStarted',
                type: 'POST',
                data:{ zipCode: zip, numFamily: 1, gender: this.$gender.filter(':checked').val() },
                cache: false
            });
        },

        backtoInfo:function(){
            $.ajax({
                url: '/clearSession',
                type: 'POST',
                cache: false,
                statusCode : {
                        200: function(){
                            window.location = "/pricing";
                            return this;
                        },
                        500: function(){
                            window.location = "/pricing";
                            return this;
                        }
                    }
            });

        },
        addToSubscribe:function(e){
            var self = this;
            e.preventDefault();
            var missingFields = false;
            var error=false;
            $(".requiredforSubscribe").each(function(){
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

        householdChange: function(e) {
            this.model.set('household', parseInt(e.currentTarget.value, 10));
        },

		initialize: function() {
			this.model = new Backbone.Model(window.resupply);
            this.model.on('change:household', this.render, this);

			this.householdList = new HouseholdList(window.pricingData);

            this.$chartContainer = this.$('.resupply-pricing-chart');
            this.$zip = this.$('#zipCode');
            this.$alert = this.$('.alert');
            this.$gender = this.$('.gender');

            this.render();
		},

		render: function() {
            var household = this.model.get('household') || 1
            var chart = this.householdList.findWhere({familySize: household}).toJSON();
            var currentPackage = this.model.get('currentPackage');
            this.$chartContainer.html(_.template(tmpl, {
                chart: chart,
                household: household,

                // note: currentPackage key only set if user is logged in
                authed: !!currentPackage,
                currentPackage: currentPackage
            }));

            // selects the current package
            this.$('.household-inputs label').removeClass('active');
            this.$('.household[value="'+household+'"]').prop('checked', true).parent().addClass('active');
		}
	});
    $(function(){ return new PricingView(); });
});
