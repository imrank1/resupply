from flask import Flask, flash, redirect, render_template, \
     request, url_for,session,jsonify     
from flask.ext.mongoengine import MongoEngine
from resupply import *
from resupply import config
from resupply.models import *
from resupply.services.userservice import *
from resupply.services.pricingService import *
from flask.ext.login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user, current_user
from flask.ext.mongoengine import DoesNotExist
import stripe
from flask import make_response 
from functools import update_wrapper 
import requests

# import resupply.services.userservice


def send_mail(to_address, from_address, subject, plaintext, html):
    r = requests.\
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

def nocache(f): 
	def new_func(*args, **kwargs): 
		resp = make_response(f(*args, **kwargs)) 
		resp.cache_control.no_cache = True 
		return resp 
	return update_wrapper(new_func, f) 


@app.route("/test")
def test():
    return render_template('test.html')


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

# @app.route("/")
# def home():
#     return render_template('home.html')


@app.route("/charge", methods=['POST'])
def charge():
    print "hellooooo"
    email = request.form['email']
    password = request.form['password']
    shippingAddress = request.form['shippingAddress']
    shippingAddress2 = request.form['shippingAddress']
    city = request.form['shippingCity']
    zipcode = request.form['shippingZip']

    customer = stripe.Customer.create(
        email=request.form['email'],
        card=request.form['stripeToken']
    )

    packageType = request.form['packageType']

    if packageType == "basic":
	    chargePrice = 1700
    elif packageType == "basicPlus":
	    chargePrice = 2000
    elif packageType == "premium":
        chargePrice = 2500
    elif packageType == "premiumPlus":
	    chargePrice = 2800


    description = "Charging customer with email : " + email + " for " + packageType + " at address :" + shippingAddress + " " + shippingAddress2 + " " + city + " " + zipcode

    charge = stripe.Charge.create(
    	customer=customer.id,
    	amount=chargePrice,
    	currency='usd',
    	description=description
    )



    createdUser = UserService.createUser(email,password,shippingAddress,shippingAddress2,city,zipcode,request.form['stripeToken'],packageType,customer.id)

    login_user(createdUser)

    send_mail(email,'imrank1@gmail.com','test mailgun resupply signup will create a template for this signup confirmation','plaintext','this is html')
	
    return render_template('pricing.html')



@app.route("/pricing")
def pricing():
	return render_template('pricing.html')

@app.route("/checkEmail",methods = ['GET'])
def checkEmail():
	count_of_email = User.objects(emailAddress=request.args.get('emailAddress')).count()
	resp = None
	if count_of_email > 0:
		data = {'available':False}
		resp = jsonify(data)
		resp.status_code = 500
	else:
		resp = jsonify({'available':True})
		resp.status_code = 200
	return resp


@app.route("/step1", methods =['POST','GET'])
def step1():
    packageType = request.form['packageType']
    return render_template('signupStep2.html',packageType=packageType,packagePrice=PricingService.getPackagePrice(packageType))



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
		createdUser = UserService.createUser(email,password,gender)

		theUser = User.objects.get(emailAddress=email)
		print "created user"
		login_user(theUser)
		print "logged in the user redirected to /signup"
		return redirect('/signup-step2')
	else:
		return render_template('home.html',passwordNoMatch=True) 

	return


#@app.route("/checkEmail",methods=['GET'])
#def checkEmail():
#    request.form['email']
#    count_of_email = User.objects(emailAddress=email).count()
#    if(count_of_email > 0 ){
#
#    }

# callback to relaad the user object        
@login_manager.user_loader
def load_user(userid):
    return User.objects.get(id=userid)



@app.route("/register")
def register():
	print "hellooo this is login"
	return render_template('login.html')

@app.route("/signin")
def signin():
    return render_template('signin2.html')

@app.route("/account")
@login_required
def login():
	user = current_user
	return render_template('account_home.html',currentPackage=user.currentPackage,zipCode=user.zipCode,address=user.address,address2=user.address2,city=user.city)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')

@app.route("/process-login",methods=['POST', 'GET'] )
def processLogin():
	email = request.form['email']
	password = request.form['password']
	user = None
	try:
		user = User.objects.get(emailAddress=email)
	except DoesNotExist:
		print "user does not exist"
		flash('Hmm looks like there is no user with that email. Have you signed up?')
		return render_template("login.html",userNotFound=True)

	if user.check_password(password):
		print "logging in the user"
		login_user(user)
		return render_template('account_home.html',currentPackage=user.currentPackage,zipCode=user.zipCode,address=user.address,address2=user.address2,city=user.city)
	else:
		print "passwords don't match"
		flash('Sorry the password you entered does not match. Need to <a href="restPassword"> reset</a> it?')
		return render_template("signin2.html",passwordNoMatch=True)


@app.route("/signup-select-package",methods=["POST"])
@login_required
def signupSelectPackage():
	packageType = request.form['packageType']
	user = current_user
	user = UserService.updateUserPackage(packageType,user)

	return render_template('signup-step3.html',key=app.config["STRIPE_PUBLISHABLE_KEY"])

#this is where i need to process the credit card information
@app.route("/signup-final",methods=["POST"])
@login_required
def signupSelectPackage():
	print "final signup process"	
	user = current_user

	return render_template('signup-step3.html')


@app.route("/updateShippingAddress",methods=["POST"])
@login_required
def updateShippingAddress():
	shippingAddress = request.form['shippingAddress']
	shippingAddress2 = request.form['shippingAddress2']
	city = request.form['shippingCity']
	zipcode = request.form['shippingZip']

	UserService.updateUserShippingAddress(current_user,shippingAddress,shippingAddress2,city,zipcode)

	data = {'updated':True}
	resp = jsonify(data)
	resp.status_code = 202
	return resp


@app.route("/requestPasswordChange",methods=["POST"])
def requestPasswordChange():
    user = current_user
    linkRef = str(user.id)[5:10]
    link = "http://resupply-staging.heroku.com/passwordChange/" + linkRef;
    data = {'link':link}
    resp = jsonify(data)
    resp.status_code = 202
    return resp











