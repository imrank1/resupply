from flask import Flask, url_for,redirect,request
from flask.ext.mongoengine import MongoEngine
from resupply import *
from resupply import config
from flask import render_template
from flask.ext.login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user
import os
import stripe



app = Flask(__name__)


env = os.environ.get('FLASK_ENV', 'development')


configuration = None
if env =='development':
	app.config["MONGODB_DB"] = config.dev['mongodb_db']
	app.config["SECRET_KEY"] = config.dev['secret_key']
	stripe.api_key=config.dev['stripe_secret_key']
elif env =='production':
	app.config["MONGODB_DB"] = config.production['mongodb_db']
	app.config["SECRET_KEY"] = config.dev['secret_key']
	app.config["MONGODB_USERNAME"] = config.production['mongodb_username']	
	app.config["MONGODB_PASSWORD"] = config.production['mongodb_password']
	app.config["MONGODB_HOST"] = config.production['mongodb_host']
	app.config["MONGODB_HOST"] = config.production['mongodb_host']
	app.config["MONGODB_PORT"] = config.production['mongodb_port']
	stripe.api_key=confg.production['stripe_secret_key']



# app.config.stripe_keys = {
#   'secret_key': 'sk_07vkIYtFhTJY68s2pipRKmlvDtiqk',
#   'publishable_key': 'pk_07vkx4yqszys5bnTNnHPSAAimkCie'
# }

# stripe.api_key = config.stripe_keys['secret_key'] 

# app.config["MONGODB_DB"] = "my_tumble_log"
# app.config["SECRET_KEY"] = "p0c0n0$Cyrus"

db = MongoEngine(app)

login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = "login"



import resupply.views
import resupply.controllers.homeController
