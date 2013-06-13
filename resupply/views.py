from flask import Flask, flash, redirect, render_template, \
    request, url_for, session, jsonify, g
from flask.ext.mongoengine import MongoEngine
from resupply import *
from resupply import config
from resupply.models import *
from resupply.services.userservice import *
from resupply.services.pricingService import *
from resupply.services.passwordChangeService import *
from resupply.services.refferalService import * 
from resupply.services.taxService import * 
from flask.ext.login import LoginManager, UserMixin, \
    login_required, login_user, logout_user, current_user
from flask.ext.mongoengine import DoesNotExist
import stripe
from flask import make_response
from functools import update_wrapper 
import requests
import os
# import resupply.services.userservice
login_manager.login_view = "/index"

env = os.environ.get('FLASK_ENV', 'development')

def send_mail(to_address, from_address, subject, plaintext, html):
    r = requests. \
        post("https://api.mailgun.net/v2/%s/messages" % 'resupply.mailgun.org',
             auth=("api", 'key-0tv5b0tr16dz-86zophipsh5htylj2h2'),
             data={
                 "from": from_address,
                 "to": to_address,
                 "subject": subject,
                 "text": plaintext,
                 "html": html
             }
    )
    return r

@app.before_request
def before_request():
   g.user = current_user

def nocache(f):
    def new_func(*args, **kwargs):
        resp = make_response(f(*args, **kwargs))
        resp.cache_control.no_cache = True
        return resp

    return update_wrapper(new_func, f)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


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
#    taxRate = TaxService.getSalesTax(zipcode)
    taxRateString = '%2f'%taxRate
    app.logger.info('sales tax for zip' + zipcode + 'determined to be:' + taxRateString)


    chargePrice = None
    taxMultiplier = 1 + taxRate

    packageType = session.get('packageType')
    app.logger.info('packageType is:' + packageType)
    chargePrice = PricingService.getPackagePrice(packageType)*100
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
    return render_template("checkout.html",name=session.get('name'),package=session.get('packageType'),email=session.get('email'),password=session.get('password'),shippingAddress=session.get('shippingAddress'),shippingAddress2=session.get('shippingAddress2'),shippingCity=session.get('city'),zipcode=session.get('zipCode'),finalPricePerMonth=session.get('finalPricePerMonth')/100,stripePlanIdentifier=session.get('stripePlanIdentifier'),city=session.get('city'),state=session.get('state'),phone=session.get('phone'),stripePublishableKey=app.config["STRIPE_PUBLISHABLE_KEY"])




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
                        send_mail(refferalObject.originatorEmailAddress, 'support@resupp.ly','We\'ve reduced your subscription amount!', 'html',couponAppliedHtml)
                        send_mail('imrank1@gmail.com', 'support@resupp.ly','We\'ve reduced your subscription amount!', 'html',couponAppliedHtml)


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

    createdUser = UserService.createUser(email, password, shippingAddress, shippingAddress2, shippingState,shippingPhone,zipcode,request.form['stripeToken'], stripePlanIdentifier, customer.id,sourceRefferer)

    RefferalService.createRefferal(createdUser.emailAddress)
    login_user(createdUser)
    emailHtml = render_template('emails/signupConfirmationEmailTemplate.html',package=PricingService.getDisplayPackage(stripePlanIdentifier),pricePerMonth=chargePrice,shippingAddress=fullAddress)
    send_mail(createdUser.emailAddress, 'support@resupp.ly',
              'Confirmation of subscription to Resupp.ly', 'html',
              emailHtml)
    send_mail('imrank1@gmail.com', 'support@resupp.ly',
              'Confirmation of subscription to Resupp.ly', 'html',
              emailHtml)

    return render_template('pricing.html')


@app.route("/testConfirmationEmail")
def confirmEmailTest():
    emailHtml = render_template('emails/signupConfirmationEmailTemplate.html',package="Premium",pricePerMonth=2000/100,
                                shippingAddress="11945 Little Seneca Parkway, Clarksburg , MD, 20871")
    send_mail('imrank1@gmail.com', 'imrank1@gmail.com',
              'Confirmation of subscription to Resupp.ly', 'html',
              emailHtml)
    return render_template("pricing.html")


@app.route("/newHome")
def newHome():
    user = current_user
    if(user.is_anonymous()==False):
        return render_template('newHome.html',loggedIn=True,emailAddress=user.emailAddress,user=g.user)
    else:
        return render_template('newHome.html',loggedIn=False,user=g.user)

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
        pricingMap = PricingService.getPricingMap(int(PricingService.getHouseHouldSizeFromPackage(user.currentPackage)))
        return render_template('pricingUpgrade.html',currentPackage=currentPackage,user=g.user,pricingMap=pricingMap)
    else:
        numFamily = session.get('houseHoldSize')
        if(numFamily==None):
            return redirect("/infoAboutYou")
        app.logger.info(numFamily)
        pricingMap = PricingService.getPricingMap(int(numFamily))
        return render_template('pricing_new.html',showGetStarted=showGetStarted,user=None,pricingMap=pricingMap)

    return render_template('pricing_new.html',showGetStarted=showGetStarted)


@app.route("/pricing2")
def pricing2():
    return render_template('pricing_new2.html')

@app.route("/pricing3")
def pricing3():
    return render_template('pricing_new3.html')

@app.route("/pricing4")
def pricing4():
    return render_template('pricing_new4.html')


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


@app.route("/step1", methods=['POST', 'GET'])
def step1():
    packageType = request.form['packageType']
    app.logger.info('in step1 the package selected is:' + packageType + 'zip code is :' + session.get('targetZipCode'))
    session['packageType'] = packageType

    return render_template('signupStep2_new.html',name=session.get('name'),package=session.get('packageType'),email=session.get('email'),password=session.get('password'),shippingAddress=session.get('shippingAddress'),
    shippingAddress2=session.get('shippingAddress2'),zipcode=session.get('targetZipCode'),finalPricePerMonth=session.get('finalPricePerMonth'),city=session.get('city'),packageType=PricingService.getDisplayPackage(packageType),packagePrice=PricingService.getPackagePrice(packageType))
    #return render_template('signupStep2_new.html', packageType=packageType,packagePrice=PricingService.getPackagePrice(packageType))

@app.route("/getStarted",methods=['POST'])
def getStarted():
    gender = request.form['gender']
    zipCode = request.form['zipCode']
    houseHoldSize = request.form['numFamily']
    canShip = True
    resp = None
    try:
        firstZip = int(zipCode[:1])
        if(UserService.canShip(firstZip)==False):
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
def upgradeConfirmation():
    user = current_user
    currentPackage = user.currentPackage
    upgradePackage = request.form['packageType']
    familySize = request.form['familySize']
    return render_template('upgradeConfirmation.html',currentPackage=PricingService.getDisplayPackage(currentPackage),upgradePackageDisplay=PricingService.getDisplayPackage(upgradePackage),upgradePackage=upgradePackage,currentPrice=PricingService.getPackagePrice(currentPackage),upgradePrice=PricingService.getPackagePrice(upgradePackage),familySize=familySize)


@app.route("/processUpgrade",methods=['POST'])
@login_required
def processUpgrade():
    user = current_user
    packageType = request.form['packageType']
    prevPackage = user.currentPackage

    taxRate = TaxService.getSalesTax(user.zipCode)
    taxRateString = '%2f'%taxRate
    app.logger.info('sales tax for zip' + user.zipCode + 'determined to be:' + taxRateString)


    chargePrice = None
    taxMultiplier = 1 + taxRate

    chargePrice = PricingService.getPackagePrice(packageType)*100

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
    emailHtml = render_template("emails/upgradeConfirmationEmail.html",newPackage=PricingService.getDisplayPackage(packageType),pricePerMonth=chargePrice/100,
                                oldPackage=PricingService.getDisplayPackage(prevPackage.split("-",1)[0]))
    send_mail(user.emailAddress, 'support@resupp.ly',
        'Resupply Upgrade Confirmation', 'html',
        emailHtml)
    send_mail(user.emailAddress, 'imrank1@gmail.com',
        'Resupply Upgrade Confirmation', 'html',
        emailHtml)
    return redirect('/account')


@app.route("/signup-step2")
@nocache
def signupStep1():
    return render_template('signup-step2.html')


@app.route("/signup2", methods=['POST'])
def signupStep2():
    print "got to the second step"
    email = request.form['email']
    gender = request.form['gender']
    zipCode = request.form['zip']
    return render_template('signup-step2.html')


@app.route("/signup-process", methods=['POST'])
@login_required
def signupStep2():
    print "got form submit"
    email = request.form['email']
    gender = request.form['gender']
    zipCode = request.form['zip']
    pricingOption = request.form['pricingOption']
    user = current_user

    user.current_package = pricingOption
    user.save()
    return render_template('pricing.html')


@app.route("/signup3")
@login_required
def signupStep3():
    return render_template('signup-step3.html')


@app.route("/signup/quick", methods=['POST', 'GET'])
def quickSignup():
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['passwordConf']
    gender = request.form['gender']
    count_of_email = User.objects(emailAddress=email).count()

    if count_of_email > 0:
        print "duplicate email"
        flash('Sorry there is an account with that email already!')
        return redirect('/')
    elif confirm_password == password:
        createdUser = UserService.createUser(email, password, gender)

        theUser = User.objects.get(emailAddress=email)
        print "created user"
        login_user(theUser)
        print "logged in the user redirected to /signup"
        return redirect('/signup-step2')
    else:
        return render_template('home.html', passwordNoMatch=True)

    return


@login_manager.user_loader
def load_user(userid):
    return User.objects.get(id=userid)



@app.route("/signin")
def signin():
    return render_template('user/login.html',user=None)




@app.route("/forgotPassword")
def forgotPassword():
    return render_template('user/forgotPassword.html',user=None)


@app.route("/account")
@login_required
def login():
    user = current_user
    refferal = Refferal.objects.get(originatorEmailAddress=user.emailAddress)
    bitlyLink = refferal.bitlyLink
    return render_template('user/account_home.html', currentPackage=PricingService.getDisplayPackage(user.currentPackage.split("-",1)[0]),numFamily=PricingService.getHouseHouldSizeFromPackage(user.currentPackage), zipCode=user.zipCode,
                           address=user.address, address2=user.address2, city=user.city,refferalCode=refferal.refferalCode,user=g.user,bitlyLink=bitlyLink)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/process-login", methods=['POST', 'GET'])
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

@app.route("/infoAboutYou",methods=["GET"])
def infoAboutYou():
    user = g.user
    session.clear()
    return render_template('infoStep.html',user=user)


@app.route("/infoAboutYouUpgrade",methods=["GET"])
@login_required
def infoAboutYouUpgrade():
    user = g.user
    return render_template('infoStepUpgrade.html',user=user,currentPackage=PricingService.getDisplayPackage(user.currentPackage.split("-",1)[0]),houseSize=PricingService.getHouseHouldSizeFromPackage(user.currentPackage))


@app.route("/introUpgrade",methods=['POST'])
@login_required
def processIntroUpgrade():
    user = g.user
    numFamily = request.form['numFamily']
    currentPackage = user.currentPackage.split("-",1)[0]
    pricingMap = PricingService.getPricingMap(int(numFamily))
    return render_template('pricingUpgrade.html',currentPackage=currentPackage,user=g.user,pricingMap=pricingMap)



@app.route("/updateShippingAddress",methods=["POST"])
@login_required
def updateShippingAddress():
    shippingAddress = request.form['shippingAddress']
    shippingAddress2 = request.form['shippingAddress2']
    zipcode = request.form['shippingZip']

    UserService.updateUserShippingAddress(current_user,shippingAddress,shippingAddress2,zipcode)

    data = {'updated':True}
    resp = jsonify(data)
    resp.status_code = 202
    return resp


@app.route('/changePassword')
def changepassword():
    try:
        linkRef = request.args.get('linkRef', '')
        resetRequest = PasswordChangeRequest.objects.get(linkRef = linkRef,used=False)
        user = User.objects.get(emailAddress = resetRequest.ownerEmailAddress)
    except Exception:
        app.logger.info("request to change password with used linkRef " + linkRef)
        return render_template('/')
    else:
        app.logger.info("showing the passwordchange form for:" + user.emailAddress)
        return render_template('why.html',userEmailAddress=user.emailAddress,linkRef = linkRef)


@app.route('/somthing/<what>',methods=['GET'])
def somthing(what):
    return render_template('why.html')


@app.route("/forgotPasswordSubmit",methods=['POST'])
def processForgotPasswordChange():
    email=request.form['email']
    try:
        user = User.objects.get(emailAddress=email)    
    except DoesNotExist: 
        return render_template ("user/forgotPassword.html",userNotFound=True,emailSent=False)
    else:
        linkRef = str(user.id)[5:10]
        now = datetime.datetime.now().microsecond
        linkRef = linkRef + str(now)
        link = app.config["passwordResetPrefix"] + linkRef;
        PasswordChangeService.createPasswordChangeRequest(user.emailAddress,linkRef)

        email =  render_template ("emails/passwordResetEmail.html",link=link)

        send_mail(user.emailAddress,'support@resupp.ly','Resupply Password Reset', 'html',email)

        send_mail('imrank1@gmail.com', 'support@resupp.ly','Resupply Password Reset', 'html',email)

        return render_template ("user/forgotPassword.html",userNotFound=False,emailSent=True)




@app.route("/requestPasswordChange",methods=["POST"])
def requestPasswordChange():
    user = current_user
    linkRef = str(user.id)[5:10]
    now = datetime.datetime.now().microsecond
    linkRef = linkRef + str(now)
    link = app.config["passwordResetPrefix"] + linkRef;
    PasswordChangeService.createPasswordChangeRequest(user.emailAddress,linkRef)


    send_mail(user.emailAddress, 'support@resupp.ly',
        'Resupply Password Link', 'plaintext',
          'Click the folowing link to reset your password' + link)


    send_mail('imrank1@gmail.com', 'support@resupp.ly',
        'Resupply Password Link', 'plaintext',
          'Click the folowing link to reset your password' + link)

    data = {'link':link}
    resp = jsonify(data)
    resp.status_code = 202
    return resp



@app.route("/handlePasswordChange", methods=["POST"])
def handlePasswordChange():
    newPassword = request.form['password']
    linkRef = request.form['linkRef']
    PasswordChangeService.updateUserPassword(linkRef,newPassword)
    res = jsonify({'passwordChanged':True})
    res.status_code = 202
    return res


@app.route("/cancelAccount",methods=["POST"])
@login_required
def cancelAccount():
    user = current_user
    UserService.cancelAccount(user)

    email =  render_template ("emails/cancelAccountConfirmationEmail.html")

    send_mail(user.emailAddress,'support@resupp.ly','Resupply Account Cancellation Confirmation', 'html',email)

    send_mail('imrank1@gmail.com', 'support@resupp.ly','Resupply Account Cancellation Confirmation', 'html',email)

    user.delete()
    logout_user()
    res = jsonify({'canceled':True})
    res.status_code = 202
    app.logger.info("closed the account for :" + user.emailAddress)
    return res

@app.route("/addToSubscribe",methods=["POST"])
def addToSubscribe():
    email = request.form['email']
    UserService.addToSubscribe(email)
    res = jsonify({'addedd':True})
    res.status_code = 200
    return res








