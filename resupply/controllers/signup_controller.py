from flask import Flask, flash, redirect, render_template, \
	request, url_for, session, jsonify, g
from flask.ext.mongoengine import MongoEngine
from resupply import *
from resupply import config
from resupply.models import *
from resupply.services import user_service
from resupply.services import pricing_service
from resupply.services import password_change_service 
from resupply.services import refferal_service 
from resupply.services import tax_service 
from resupply.services import email_service
from flask.ext.login import LoginManager, UserMixin, \
	login_required, login_user, logout_user, current_user
from flask.ext.mongoengine import DoesNotExist
import stripe
from flask import make_response
from functools import update_wrapper 
import requests
import os


@app.route("/stageCharge" ,methods=['POST'])
def stageCharge():
	name = request.form['name']
	email = request.form['email']
	password = request.form['password']
	shippingAddress = request.form['shippingAddress']
	shippingAddress2 = request.form['shippingAddress']
	city = request.form['shippingCity']
	zipcode = request.form['shippingZip']
	refferal = session.get('refferalCode')
	phone = request.form['shippingPhone']
	shippingState = request.form['shippingState']
	session['name'] = name
	session['email']=email
	session['password'] = password
	session['shippingAddress'] = shippingAddress
	session['shippingAddress2'] = shippingAddress2
	session['city'] = city
	session['zipCode'] = zipcode
	session['password'] = password
	session['phone'] = phone
	session['state'] = shippingState

	taxRate = None
	if shippingState == 'VA':
		taxRate = 0.06
	else:
		taxRate = 0.0
#    taxRate = tax_service.getSalesTax(zipcode)
	taxRateString = '%2f'%taxRate
	app.logger.info('sales tax for zip' + zipcode + 'determined to be:' + taxRateString)


	chargePrice = None
	taxMultiplier = 1 + taxRate

	packageType = session.get('packageType')
	app.logger.info('packageType is:' + packageType)
	chargePrice = pricing_service.getPackagePrice(packageType)*100
	finalPrice = chargePrice * taxMultiplier
	stripePlanIdentifier = packageType + '-' + '%.2f'%chargePrice + '-' + '%.2f'%taxMultiplier +'-' + zipcode + '-' + shippingState
	currentStripePlans = stripe.Plan.all()
	targetStripePlan = None
	for plan in currentStripePlans.data:
		if plan.name == stripePlanIdentifier:
			app.logger.info("Found existing stripe plan:" + stripePlanIdentifier)
			targetStripePlan = plan
			break

	if targetStripePlan == None:
		app.logger.info("Creating new stripe plan for:"  + stripePlanIdentifier)
		stripe.Plan.create(
			amount='%.0f'%finalPrice,
			interval='month',
			name=stripePlanIdentifier,
			currency='usd',
			id=stripePlanIdentifier)

	app.logger.info('package price is :' + '%.2f'%chargePrice)
	app.logger.info('with tax package price is : ' + '%.2f'%finalPrice)

	session['stripePlanIdentifier'] = stripePlanIdentifier
	session['finalPricePerMonth'] = round(finalPrice,2)
	session.modified = True
	app.logger.info(session)

	res = jsonify({'staged':True})
	res.status_code = 200
	return res



@app.route("/finalStep",methods=['GET'])
def finalStep():
	return render_template("signup/checkout.html",name=session.get('name'),package=session.get('packageType'),email=session.get('email'),password=session.get('password'),shippingAddress=session.get('shippingAddress'),shippingAddress2=session.get('shippingAddress2'),shippingCity=session.get('city'),zipcode=session.get('zipCode'),finalPricePerMonth=session.get('finalPricePerMonth')/100,stripePlanIdentifier=session.get('stripePlanIdentifier'),city=session.get('city'),state=session.get('state'),phone=session.get('phone'),stripePublishableKey=app.config["STRIPE_PUBLISHABLE_KEY"])



@app.route("/checkEmail", methods=['GET'])
def checkEmail():
    count_of_email = User.objects(emailAddress=request.args.get('emailAddress')).count()
    resp = None
    if count_of_email > 0:
        data = {'available': False}
        resp = jsonify(data)
        resp.status_code = 500
    else:
        resp = jsonify({'available': True})
        resp.status_code = 200
    return resp


@app.route("/charge", methods=['POST'])
def charge():
	app.logger.info("starting charge")
	email = request.form['email']
	password = request.form['password']
	shippingAddress = request.form['shippingAddress']
	shippingAddress2 = request.form['shippingAddress2']
	zipcode = request.form['shippingZip']
	refferal = session.get('refferalCode')
	phone = request.form['shippingPhone']
	shippingState = request.form['shippingState']
	shippingPhone = request.form['shippingPhone']
	sourceRefferer = None
	if(refferal):
		refferalCode = refferal.split('-')[1]
		refferalObject = Refferal.objects.get(refferalCode=refferalCode)
		if(refferalObject):
			sourceRefferer = refferalObject.originatorEmailAddress
			refferUser = User.objects.get(emailAddress=refferalObject.originatorEmailAddress)
			if(refferUser):
				if(refferUser.reducedPrice==False):
					refferStripeCustomer = stripe.Customer.retrieve(refferUser.stripeCustomerId)
					if(refferStripeCustomer):
						refferStripeCustomer.coupon = "3month25PCTOff"
						refferStripeCustomer.save()
						refferUser.reducedPrice = True
						refferrUser.save()
						couponAppliedHtml = render_template('emails/couponApplied.html',amount=25)
						email_service.send_mail(refferalObject.originatorEmailAddress, 'support@resupp.ly','We\'ve reduced your subscription amount!', 'html',couponAppliedHtml)
						email_service.send_mail('imrank1@gmail.com', 'support@resupp.ly','We\'ve reduced your subscription amount!', 'html',couponAppliedHtml)


	stripePlanIdentifier = session.get('stripePlanIdentifier')

	packageType = stripePlanIdentifier
	chargePrice = request.form['finalPrice']

	description = "Charging customer with email : " + email + " for " + packageType + " at address :" + shippingAddress + " " + shippingAddress2  + " " + zipcode
	fullAddress = shippingAddress + ',' 
	if shippingAddress2 != None :
		fullAddress = fullAddress + shippingAddress2
  

	fullAddress = ',' + fullAddress  + ',' + zipcode

	customer = stripe.Customer.create(
		email=request.form['email'],
		card=request.form['stripeToken'],
		plan=stripePlanIdentifier,
		description=description)

	createdUser = user_service.createUser(email, password, shippingAddress, shippingAddress2, shippingState,shippingPhone,zipcode,request.form['stripeToken'], stripePlanIdentifier, customer.id,sourceRefferer)

	refferal_service.createRefferal(createdUser.emailAddress)
	login_user(createdUser)
	emailHtml = render_template('emails/signupConfirmationEmailTemplate.html',package=pricing_service.getDisplayPackage(stripePlanIdentifier),pricePerMonth=chargePrice,shippingAddress=fullAddress)
	email_service.send_mail(createdUser.emailAddress, 'support@resupp.ly',
			  'Confirmation of subscription to Resupp.ly', 'html',
			  emailHtml)
	email_service.send_mail('imrank1@gmail.com', 'support@resupp.ly',
			  'Confirmation of subscription to Resupp.ly', 'html',
			  emailHtml)

	return redirect('account')


@app.route("/step1", methods=['POST', 'GET'])
def step1():
	packageType = request.form['packageType']
	app.logger.info('in step1 the package selected is:' + packageType + 'zip code is :' + session.get('targetZipCode'))
	session['packageType'] = packageType

	return render_template('signup/signupStep2.html',name=session.get('name'),package=session.get('packageType'),email=session.get('email'),password=session.get('password'),shippingAddress=session.get('shippingAddress'),
	shippingAddress2=session.get('shippingAddress2'),zipcode=session.get('targetZipCode'),finalPricePerMonth=session.get('finalPricePerMonth'),city=session.get('city'),packageType=pricing_service.getDisplayPackage(packageType),packagePrice=pricing_service.getPackagePrice(packageType))



@app.route("/getStarted",methods=['POST'])
def getStarted():
	gender = request.form['gender']
	zipCode = request.form['zipCode']
	houseHoldSize = request.form['numFamily']
	canShip = True
	resp = None
	try:
		firstZip = int(zipCode[:1])
		if(user_service.canShip(firstZip)==False):
			app.logger.info("We can't ship  to " + zipCode)
			canShip = False
			resp = jsonify({'available': canShip})
			resp.status_code = 500
			return resp
		if(zipCode and houseHoldSize):
			session['targetZipCode'] = zipCode
			session['houseHoldSize'] = houseHoldSize
			session['gender'] = gender
			resp = jsonify({'available': canShip})
			resp.status_code = 200
			return resp
	except Exception:
		canShip = False
		resp = jsonify({'available': canShip})
		resp.status_code = 500
		return resp
	

@app.route("/infoAboutYou",methods=["GET"])
def infoAboutYou():
	user = g.user
	session.clear()
	return render_template('product/infoStep.html',user=user)




@app.route("/addToSubscribe",methods=["POST"])
def addToSubscribe(self):
	email = request.form['email']
	user_service.addToSubscribe(email)
	res = jsonify({'addedd':True})
	res.status_code = 200
	return res
