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


    # def get_id(self):
    #     return unicode(self.id)

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'emailAddress'],
        'ordering': ['-created_at']
    }
