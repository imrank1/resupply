from flask import Flask, url_for,redirect,request
from flask.ext.mongoengine import MongoEngine
from resupply import *
from flask import render_template

@app.route("/")
def hello():
    return render_template('index.html')