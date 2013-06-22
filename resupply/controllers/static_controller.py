from flask import Flask, url_for,redirect,request,session, g
from flask.ext.mongoengine import MongoEngine
from resupply import *
from flask import render_template
from flask.ext.login import LoginManager, UserMixin, \
	login_required, login_user, logout_user, current_user
from resupply.services import pricing_service

@app.route("/")
def root():
	user = current_user
	if(user.is_anonymous()==False):
		return redirect("/account")
	else:
		fbParam = request.args.get('fb_ref')
		if(fbParam):
			app.logger.info("received fb-ref= " + fbParam)
			session['refferalCode']=fbParam
	return render_template('public/index.html')

@app.route("/index")
def index(self):
	return redirect("/")


@app.route("/about")
def about():
	return render_template('public/about.html')

#ehh this might fit somewhere else.
@app.route("/pricing")
def pricing():
	app.logger.info('showing the pricing page fadfa')
	refferalCode = None
	refferalCode = session.get('refferalCode')
	targetZipCode = None
	targetZipCode = session.get('targetZipCode')
	showGetStarted = False
	if(refferalCode):
		app.logger.info("refferal in session is  " + refferalCode)

	if(targetZipCode==None):
		showGetStarted=True
		app.logger.info("showing getStartedModal on pricing screen")

	user = current_user
	if(user.is_anonymous()==False):
		app.logger.info("there is a current user with " + user.currentPackage)
		currentPackage = user.currentPackage.split("-",1)[0]
		pricingMap = pricing_service.getPricingMap(int(pricing_service.getHouseHouldSizeFromPackage(user.currentPackage)))
		return render_template('product/pricing.html',currentPackage=currentPackage,user=g.user,pricingMap=pricingMap)
	else:
		numFamily = session.get('houseHoldSize')
		if(numFamily==None):
			return redirect("/infoAboutYou")
		app.logger.info(numFamily)
		pricingMap = pricing_service.getPricingMap(int(numFamily))
		return render_template('product/pricing.html',showGetStarted=showGetStarted,user=None,pricingMap=pricingMap)

	return render_template('product/pricing.html',showGetStarted=showGetStarted)


@app.route('/pricingChart')
def pricingChart():
	user = current_user
	currentPackage = ''
	refferalCode = session.get('refferalCode')
	zipcode = session.get('targetZipCode') or 0
	household = session.get('houseHoldSize') or 0
	if(not user.is_anonymous()):
		household = int(pricing_service.getHouseHouldSizeFromPackage(user.currentPackage))
		currentPackage = user.currentPackage.split("-",1)[0]
        if hasattr(user, 'zipCode'):
            zipcode = user.zipCode

	return render_template(
		'product/pricing_chart.html',
		user=user,
		zipcode=zipcode,
		household=household,
		currentPackage=currentPackage,
		pricingData=pricing_service.getFullPricingData()
	)
