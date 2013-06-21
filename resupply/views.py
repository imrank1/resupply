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




login_manager.login_view = "/index"

env = os.environ.get('FLASK_ENV', 'development')

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



@app.route("/testConfirmationEmail")
def confirmEmailTest():
    emailHtml = render_template('emails/signupConfirmationEmailTemplate.html',package="Premium",pricePerMonth=2000/100,
                                shippingAddress="11945 Little Seneca Parkway, Clarksburg , MD, 20871")
    email_service.send_mail('imrank1@gmail.com', 'imrank1@gmail.com',
              'Confirmation of subscription to Resupp.ly', 'html',
              emailHtml)
    return render_template("index.html")


@app.route("/home")
def home():
    user = current_user
    if(user.is_anonymous()==False):
        return render_template('public/index.html',loggedIn=True,emailAddress=user.emailAddress,user=g.user)
    else:
        return render_template('public/index.html',loggedIn=False,user=g.user)



@login_manager.user_loader
def load_user(userid):
    return User.objects.get(id=userid)



@app.route("/signin")
def signin():
    return render_template('user/login.html',user=None)




@app.route("/forgotPassword")
def forgotPassword():
    return render_template('user/forgotPassword.html',user=None)



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/testemail",methods=["GEt"])
def testEmail():
    email_service.send_mail('imrank1@gmail.com', 'support@resupp.ly',
        'Test', 'plaintext',
          'Click the folowing link to reset your password ')
    return redirect('/')

