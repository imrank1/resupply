from flask.ext.mongoengine import MongoEngine
from resupply.models import *
import stripe
from flask import Flask
import bitly_api
import urllib
import os


def createRefferal(emailAddress):
	refferal = Refferal(originatorEmailAddress=emailAddress)
	code = str(refferal.id)[5:10]
	now = datetime.datetime.now().microsecond
	code = code + str(now)
	refferal.refferalCode = code 
 	bitly = bitly_api.Connection(access_token="b9aa357f2106667319586b4d47b30441553e4098")
 	originalLink  = "http://www.getresupply.com/?rsupplySrc=" + code
 	data = bitly.shorten(originalLink)
 	refferal.bitlyLink = data["hash"]
	refferal.save()
	return refferal