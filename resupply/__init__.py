from flask import Flask, url_for,redirect,request
from flask.ext.mongoengine import MongoEngine
from resupply import *
from resupply import config
from flask import render_template
from flask.ext.login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user
import os
import stripe

from flask_sslify import SSLify

app = Flask(__name__)

env = os.environ.get('FLASK_ENV', 'development')

configuration = None
if env =='development':
	app.config["SECRET_KEY"] = config.dev['secret_key']
	app.config["STRIPE_PUBLISHABLE_KEY"] = config.dev['stripe_publishable_key']
	stripe.api_key=config.dev['stripe_secret_key']
	app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
	app.config["passwordResetPrefix"] = config.dev['passwordResetPrefix']
	app.config["MONGODB_DB"] = config.dev['mongodb_db']
	app.config["SECRET_KEY"] = config.dev['secret_key']
	app.config["MONGODB_USERNAME"] = config.dev['mongodb_username']	
	app.config["MONGODB_PASSWORD"] = config.dev['mongodb_password']
	app.config["MONGODB_HOST"] = config.dev['mongodb_host']
	app.config["MONGODB_PORT"] = config.dev['mongodb_port']
	app.config["checkoutRedirect"] = config.dev['checkoutRedirect']
elif env =='production':
	app.config["MONGODB_DB"] = config.production['mongodb_db']
	app.config["SECRET_KEY"] = config.production['secret_key']
	app.config["MONGODB_USERNAME"] = config.production['mongodb_username']	
	app.config["MONGODB_PASSWORD"] = config.production['mongodb_password']
	app.config["MONGODB_HOST"] = config.production['mongodb_host']
	app.config["MONGODB_HOST"] = config.production['mongodb_host']
	app.config["MONGODB_PORT"] = config.production['mongodb_port']
	app.config["STRIPE_PUBLISHABLE_KEY"] = config.production['stripe_publishable_key']
	app.config["passwordResetPrefix"] = config.production['passwordResetPrefix']
	app.config["checkoutRedirect"] = config.production['checkoutRedirect']
	stripe.api_key=config.production['stripe_secret_key']

app.config["bitlyAccessToken"] = "b9aa357f2106667319586b4d47b30441553e4098"
sslify = SSLify(app)


db = MongoEngine(app)

login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = "login"



import resupply.views
from resupply.controllers.account_view import *
from resupply.controllers.signup_view import * 
from resupply.controllers.static_view import * 