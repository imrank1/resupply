from flask.ext.mongoengine import MongoEngine
from resupply.models import *

class UserService:
	@staticmethod
	def createUser(emailAddress,password,gender):
		user = User(emailAddress=emailAddress,gender=gender)
		user.set_password(password)
		user.save()
		return user

	@staticmethod
	def updateUserPackage(packageType,user):
		user.setPackage(packageType)
		user.save()
		return user
