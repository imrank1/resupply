from flask import Flask, url_for,redirect,request,session
from flask.ext.mongoengine import MongoEngine
from resupply import *
from flask import render_template

@app.route("/")
def hello():
	fbParam = request.args.get('fb_ref')
	if(fbParam):
		app.logger.info("received fb-ref= " + fbParam)
		session['refferalCode']=fbParam

	return render_template('newHome.html')

@app.route("/index")
def index():
	return render_template('newHome.html')