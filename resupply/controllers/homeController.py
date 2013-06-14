from flask import Flask, url_for,redirect,request,session
from flask.ext.mongoengine import MongoEngine
from resupply import *
from flask import render_template
from flask.ext.login import LoginManager, UserMixin, \
    login_required, login_user, logout_user, current_user


@app.route("/")
def hello():
	user = current_user
	if(user.is_anonymous()==False):
		return redirect("/account")   
	else:
		fbParam = request.args.get('fb_ref')
		if(fbParam):
			app.logger.info("received fb-ref= " + fbParam)
			session['refferalCode']=fbParam
	return render_template('public/newHome.html')

@app.route("/index")
def index():
	return redirect("/")
