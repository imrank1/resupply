from flask import Flask, url_for,redirect,request,session,jsonify, g
from flask.ext.mongoengine import MongoEngine
from resupply import *
from flask import render_template
from flask.ext.login import LoginManager, UserMixin, \
	login_required, login_user, logout_user, current_user
from resupply.models import *
from resupply.services import user_service
from resupply.services import pricing_service
from resupply.services import password_change_service 
from resupply.services import refferal_service 
from resupply.services import tax_service 
from resupply.services import email_service

@app.route("/account")
@login_required
def account():
	user = current_user
	refferal = Refferal.objects.get(originatorEmailAddress=user.emailAddress)
	bitlyLink = refferal.bitlyLink
	return render_template('user/account_home.html', currentPackage=pricing_service.getDisplayPackage(user.currentPackage.split("-",1)[0]),numFamily=pricing_service.getHouseHouldSizeFromPackage(user.currentPackage), zipCode=user.zipCode,
							   address=user.address, address2=user.address2, city=user.city,refferalCode=refferal.refferalCode,user=g.user,bitlyLink=bitlyLink)


@app.route("/process-login")
def processLogin():
	email = request.form['email']
	password = request.form['password']
	user = None
	try:
		user = User.objects.get(emailAddress=email)
	except DoesNotExist:
		app.logger.info("Failed attempt to login for email:" + email)
		flash('Hmm looks like there is no user with that email. Have you signed up?')
		return render_template("user/login.html", userNotFound=True)

	if user.check_password(password):
		app.logger.info("logging in the user:" + user.emailAddress)
		login_user(user)
		return redirect("/account")
	else:
		app.logger.info("Bad password supplied for user:" + email)
		flash('Sorry the password you entered does not match. Need to <a href="/resetPassword"> reset</a> it?')
		return render_template("user/login.html", passwordNoMatch=True)

@app.route("/getStartedUpgrade",methods=['POST'])
def getStartedUpgrade():
	houseHoldSize = request.form['numFamily']
	canShip = True
	resp = None

	if(zipCode and houseHoldSize):
		session['houseHoldSize'] = houseHoldSize
		resp = jsonify({'available': canShip})
		resp.status_code = 200
		return resp

		@app.route("/confirmUpgrade",methods=['POST'])
		@login_required
		def upgradeConfirmation( ):
			user = current_user
			currentPackage = user.currentPackage
			upgradePackage = request.form['packageType']
			familySize = request.form['familySize']
			return render_template('product/upgradeConfirmation.html',currentPackage=pricing_service.getDisplayPackage(currentPackage),upgradePackageDisplay=pricing_service.getDisplayPackage(upgradePackage),upgradePackage=upgradePackage,currentPrice=pricing_service.getPackagePrice(currentPackage),upgradePrice=pricing_service.getPackagePrice(upgradePackage),familySize=familySize)


@app.route("/processUpgrade",methods=['POST'])
@login_required
def processUpgrade( ):
	user = current_user
	packageType = request.form['packageType']
	prevPackage = user.currentPackage

	taxRate = tax_service.getSalesTax(user.zipCode)
	taxRateString = '%2f'%taxRate
	app.logger.info('sales tax for zip' + user.zipCode + 'determined to be:' + taxRateString)


	chargePrice = None
	taxMultiplier = 1 + taxRate

	chargePrice = pricing_service.getPackagePrice(packageType)*100

	finalPrice = chargePrice * taxMultiplier
	stripePlanIdentifier = packageType + '-' + '%.2f'%chargePrice + '-' + '%.2f'%taxMultiplier +'-' + user.zipCode
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

	app.logger.info('package price upgrade is :' + '%.2f'%chargePrice)
	app.logger.info('with tax package upgrade  price is : ' + '%.2f'%finalPrice)

	customer =  stripe.Customer.retrieve(user.stripeCustomerId)
	customer.update_subscription(plan=stripePlanIdentifier)
	user.currentPackage = stripePlanIdentifier
	user.save()
	emailHtml = render_template("emails/upgradeConfirmationEmail.html",newPackage=pricing_service.getDisplayPackage(packageType),pricePerMonth=chargePrice/100,
								oldPackage=pricing_service.getDisplayPackage(prevPackage.split("-",1)[0]))
	email_service.send_mail(user.emailAddress, 'support@resupp.ly',
		'Resupply Upgrade Confirmation', 'html',
		emailHtml)
	email_service.send_mail(user.emailAddress, 'imrank1@gmail.com',
		'Resupply Upgrade Confirmation', 'html',
		emailHtml)
	return redirect('/account')





@app.route("/infoAboutYouUpgrade",methods=["GET"])
@login_required
def infoAboutYouUpgrade( ):
	user = g.user
	return render_template('product/infoStepUpgrade.html',user=user,currentPackage=pricing_service.getDisplayPackage(user.currentPackage.split("-",1)[0]),houseSize=pricing_service.getHouseHouldSizeFromPackage(user.currentPackage))


@app.route("/introUpgrade",methods=['POST'])
@login_required
def introUpgradeSubmit( ):
	user = g.user
	numFamily = request.form['numFamily']
	currentPackage = user.currentPackage.split("-",1)[0]
	pricingMap = pricing_service.getPricingMap(int(numFamily))
	return render_template('product/pricing.html',currentPackage=currentPackage,user=g.user,pricingMap=pricingMap)



@app.route("/updateShippingAddress",methods=["POST"])
@login_required
def updateShippingAddress( ):
	shippingAddress = request.form['shippingAddress']
	shippingAddress2 = request.form['shippingAddress2']
	zipcode = request.form['shippingZip']

	user_service.updateUserShippingAddress(current_user,shippingAddress,shippingAddress2,zipcode)

	data = {'updated':True}
	resp = jsonify(data)
	resp.status_code = 202
	return resp


@app.route('/changePassword')
def changepassword( ):
	try:
		linkRef = request.args.get('linkRef', '')
		resetRequest = PasswordChangeRequest.objects.get(linkRef = linkRef,used=False)
		user = User.objects.get(emailAddress = resetRequest.ownerEmailAddress)
	except Exception:
		app.logger.info("request to change password with used linkRef " + linkRef)
		return render_template('/')
	else:
		app.logger.info("showing the passwordchange form for:" + user.emailAddress)
		return render_template('user/passwordChangeForm.html',userEmailAddress=user.emailAddress,linkRef = linkRef)



@app.route("/requestPasswordChange",methods=["POST"])
def requestPasswordChangeSubmit( ):
	user = current_user
	linkRef = str(user.id)[5:10]
	now = datetime.datetime.now().microsecond
	linkRef = linkRef + str(now)
	link = app.config["passwordResetPrefix"] + '?linkRef=' + linkRef;
	password_change_service.createPasswordChangeRequest(user.emailAddress,linkRef)


	email_service.send_mail(user.emailAddress, 'support@resupp.ly',
		'Resupply Password Link', 'plaintext',
		  'Click the folowing link to reset your password ' + link)


	email_service.send_mail('imrank1@gmail.com', 'support@resupp.ly',
		'Resupply Password Link', 'plaintext',
		  'Click the folowing link to reset your password ' + link)

	data = {'link':link}
	resp = jsonify(data)
	resp.status_code = 202
	return resp



@app.route("/handlePasswordChange", methods=["POST"])
def handlePasswordChange( ):
	newPassword = request.form['password']
	linkRef = request.form['linkRef']
	password_change_service.updateUserPassword(linkRef,newPassword)
	res = jsonify({'passwordChanged':True})
	res.status_code = 202
	return res


@app.route("/cancelAccount",methods=["POST"])
@login_required
def cancelAccountSubmit( ):
	user = current_user
	user_service.cancelAccount(user)

	email =  render_template ("emails/cancelAccountConfirmationEmail.html")

	email_service.send_mail(user.emailAddress,'support@resupp.ly','Resupply Account Cancellation Confirmation', 'html',email)

	email_service.send_mail('imrank1@gmail.com', 'support@resupp.ly','Resupply Account Cancellation Confirmation', 'html',email)

	user.delete()
	logout_user()
	res = jsonify({'canceled':True})
	res.status_code = 202
	app.logger.info("closed the account for :" + user.emailAddress)
	return res


@app.route("/forgotPasswordSubmit",methods=['POST'])
def forgotPasswordSubmit( ):
	email=request.form['email']
	try:
		user = User.objects.get(emailAddress=email)    
	except DoesNotExist: 
		return render_template ("user/forgotPassword.html",userNotFound=True,emailSent=False)
	else:
		linkRef = str(user.id)[5:10]
		now = datetime.datetime.now().microsecond
		linkRef = linkRef + str(now)
		link = app.config["passwordResetPrefix"] + '?linkRef=' + linkRef;
		password_change_service.createPasswordChangeRequest(user.emailAddress,linkRef)

		email =  render_template ("emails/passwordResetEmail.html",link=link)

		email_service.send_mail(user.emailAddress,'support@resupp.ly','Resupply Password Reset', 'html',email)

		email_service.send_mail('imrank1@gmail.com', 'support@resupp.ly','Resupply Password Reset', 'html',email)

		return render_template ("user/forgotPassword.html",userNotFound=False,emailSent=True)
