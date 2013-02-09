from flask.ext.mongoengine import MongoEngine
from resupply.models import *

class UserService:
	@staticmethod
	def createUser(emailAddress,password,address,address2,city,zipCode,stripeToken,package,stripeCustomerId):
		user = User(emailAddress=emailAddress,address=address,address2=address2,city=city,zipCode=zipCode,stripeToken=stripeToken,currentPackage=package,stripeCustomerId=stripeCustomerId)
		user.set_password(password)
		user.save()
		return user

	@staticmethod
	def updateUserPackage(packageType,user):
		user.setPackage(packageType)
		user.save()
		return user
