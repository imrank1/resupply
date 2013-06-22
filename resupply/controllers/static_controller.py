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

@app.route("/contact")
def contact():
    return render_template('public/contact.html')

@app.route("/about")
def about():
	return render_template('public/about.html')

@app.route("/privacy-policy")
def privacy():
    return render_template('public/privacy.html')

@app.route("/terms-of-service")
def terms():
    return render_template('public/terms.html')

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

