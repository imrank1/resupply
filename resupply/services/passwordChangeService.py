from flask.ext.mongoengine import MongoEngine
from resupply.models import *
import datetime

class PasswordChangeService:
    @staticmethod
    def createPasswordChangeReqest(ownerEmailAddress,linkRef):
        changeRequest = PasswordChangeRequest(ownerEmailAddress=ownerEmailAddress,linkRef=linkRef)
        changeRequest.save()
        return changeRequest

    @staticmethod
    def updateUserPassword(linkRef,user,newPassword):
        changeRequest =PasswordChangeRequest.objects.get(ownerEmailAddress=user.emailAddress,linkRef = linkRef)
        user.set_password(user,newPassword)
        user.save()
        changeRequest.passwordResetAt(datetime.datetime.now)
        changeRequest.save()
        return user

    @staticmethod
    def updateUserShippingAddress(user,address,address2,zipcode,city):
        user.address = address
        user.address2 = address2
        user.zipCode = zipcode
        user.city = city
        user.save()
        return user
