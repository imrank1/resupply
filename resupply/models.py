import datetime
from flask import url_for
from resupply import db

from werkzeug.security import generate_password_hash,check_password_hash
from flask.ext.login import LoginManager, UserMixin, \
								login_required, login_user, logout_user

class User(db.Document,UserMixin):
	created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
	emailAddress = db.StringField(max_length=255, required=True)
	firstName = db.StringField(max_length=255, required=False)
	lastName = db.StringField(max_length=255, required=False)
	password_hash= db.StringField(max_length=255, required=True)
	current_package= db.StringField(max_length=255,required=False)
	gender = db.StringField(max_length=255,required=False)
	zipCode = db.StringField(max_length=255, required=False)
	address = db.StringField(max_length=255, required=False)
	address2 = db.StringField(max_length=255, required=False)
	city = db.StringField(max_length=255, required=False)
	stripeCustomerId = db.StringField(max_length=255, required=False)
	stripeToken = db.StringField(max_length=255, required=False)
	currentPackage = db.StringField(max_length=255, required=False)
	closedAccount = db.BooleanField(required=False)
	viaRefferal = db.BooleanField(required=False)
	refferedBy = db.StringField(required=False)
	reducedPrice = db.BooleanField(required=False)



	def __unicode__(self):
		return self.id

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def setPackage(self,package):
		self.current_package = package

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return "%s/%s" % (self.id, self.emailAddress)

	meta = {
		'allow_inheritance': True,
		'indexes': ['-created_at', 'emailAddress'],
		'ordering': ['-created_at']
	}

class CancelledAccount(db.Document):
	created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
	emailAddress = db.StringField(max_length=255, required=True)
	packageAtTimeOfCancellation = db.StringField(max_length=255, required=True)

	def __unicode__(self):
		return self.id

	def __repr__(self):
		return "%s/%s" % (self.id, self.emailAddress)

	meta = {
		'allow_inheritance': True,
		'indexes': ['-created_at', 'emailAddress'],
		'ordering': ['-created_at']
	}




class PasswordChangeRequest(db.Document):
	created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
	ownerEmailAddress = db.StringField(max_length=255, required=True)
	linkRef = db.StringField(max_length=255,required=False)
	passwordResetAt = db.DateTimeField(required=False)
	used = db.BooleanField(required=False)

	def __unicode__(self):
		return self.id

	def __repr__(self):
		return "%s/%s" % (self.id, self.ownerEmailAddress)


	meta = {
		'allow_inheritance': True,
		'indexes': ['-created_at', 'ownerEmailAddress'],
		'ordering': ['-created_at']
	}

class Refferal(db.Document):
	created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
	originatorEmailAddress = db.StringField(max_length=255, required=True)
	refferalCode = db.StringField(max_length=255,required=False)
	bitlyLink = db.StringField(max_length=255,required=False)
	countUsed = db.IntField(required=False)
	def __unicode__(self):
		return self.id

	def __repr__(self):
		return "%s/%s" % (self.id, self.originatorEmailAddress)

	meta = {
		'allow_inheritance': True,
		'indexes': ['-created_at', 'originatorEmailAddress'],
		'ordering': ['-created_at']
	}

class Subscriber(db.Document):
	created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
	emailAddress = db.StringField(max_length=255, required=True)
	
	def __unicode__(self):
		return self.id

	def __repr__(self):
		return "%s/%s" % (self.id, self.emailAddress)

	meta = {
		'allow_inheritance': True,
		'indexes': ['-created_at', 'emailAddress'],
		'ordering': ['-created_at']
	}

class ZipCodeTax(db.Document):
	created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
	zipCode = db.IntField(required=True)
	taxRate = db.FloatField(required=True)
	def __unicode__(self):
		return self.id

	def __repr__(self):
		return "%s/%s" % (self.id, self.zipCode)


	meta = {
		'allow_inheritance': True,
		'indexes': ['-created_at', 'zipCode'],
		'ordering': ['-created_at']
	}	

