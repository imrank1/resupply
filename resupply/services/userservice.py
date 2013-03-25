from flask.ext.mongoengine import MongoEngine
from resupply.models import *
import stripe
from flask import Flask


class UserService:
	@staticmethod
	def createUser(emailAddress, password, address, address2, city, zipCode, stripeToken, package, stripeCustomerId,sourceRefferer):
		user = User(emailAddress=emailAddress, address=address, address2=address2, city=city, zipCode=zipCode,
					stripeToken=stripeToken, currentPackage=package, stripeCustomerId=stripeCustomerId,refferedBy=sourceRefferer,reducedPrice=False)
		user.set_password(password)
		user.save()
		return user

	@staticmethod
	def updateUserPackage(packageType, user):
		user.setPackage(packageType)
		user.save()
		return user

	@staticmethod
	def updateUserShippingAddress(user, address, address2, zipcode, city):
		user.address = address
		user.address2 = address2
		user.zipCode = zipcode
		user.city = city
		user.save()
		return user


	@staticmethod
	def cancelAccount(user):
		cancelledAccount = CancelledAccount(emailAddress=user.emailAddress,
											packageAtTimeOfCancellation=user.currentPackage)
		customer = stripe.Customer.retrieve(user.stripeCustomerId)
		if (customer):
			customer.cancel_subscription()
		else:
			app.logger.info('could not find a customer in stripe with customer id ' + user.stripeCustomerId)
		cancelledAccount.save()
		user.closedAccount = True
		user.save()

		return cancelledAccount
