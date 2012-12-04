import datetime
from flask import url_for
from resupply import db

from werkzeug.security import generate_password_hash,check_password_hash


class User(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    emailAddress = db.StringField(max_length=255, required=True)
    firstName = db.StringField(max_length=255, required=True)
    lastName = db.StringField(max_length=255, required=True)
    password_hash= db.StringField(max_length=255, required=True) 

    def __unicode__(self):
        return self.emailAddress


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'emailAddress'],
        'ordering': ['-created_at']
    }

    

class Comment(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    body = db.StringField(verbose_name="Comment", required=True)
    author = db.StringField(verbose_name="Name", max_length=255, required=True)