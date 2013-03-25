from flask.ext.mongoengine import MongoEngine
from resupply.models import *
import stripe
from flask import Flask



class RefferalService:
	@staticmethod
	def createRefferal(emailAddress):
		refferal = Refferal(originatorEmailAddress=emailAddress)
		code = str(refferal.id)[5:10]
		now = datetime.datetime.now().microsecond
		code = code + str(now)
		refferal.refferalCode = code 
		refferal.save()
		return refferal