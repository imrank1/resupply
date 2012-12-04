from flask import Flask, url_for,redirect,request
from flask.ext.mongoengine import MongoEngine
from resupply import *
from flask import render_template

# app = Flask(__name__)
# app.config["MONGODB_DB"] = "my_tumble_log"
# app.config["SECRET_KEY"] = "KeepThisS3cr3t"
# app.config.['DEBUG'] = True

# db = MongoEngine(app)

