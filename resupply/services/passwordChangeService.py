from flask.ext.mongoengine import MongoEngine
from resupply.models import *
import datetime

class PasswordChangeService:
    @staticmethod
    def createPasswordChangeRequest(ownerEmailAddress,linkRef):
        changeRequest = PasswordChangeRequest(ownerEmailAddress=ownerEmailAddress,linkRef=linkRef,used=False)
        changeRequest.save()
        return changeRequest

    @staticmethod
    def updateUserPassword(linkRef,newPassword):
        print "linkRef is " + linkRef
        changeRequest = PasswordChangeRequest.objects.get(linkRef=linkRef,used=False)
        if(changeRequest):
            user = User.objects.get(emailAddress=changeRequest.ownerEmailAddress)
            user.set_password(newPassword)
            user.save()
            changeRequest.passwordResetAt = datetime.datetime.now()
            changeRequest.used = True
            changeRequest.save()
        else:
            raise Exception("change request already used")
        return user

    @staticmethod
    def updateUserShippingAddress(user,address,address2,zipcode,city):
        user.address = address
        user.address2 = address2
        user.zipCode = zipcode
        user.city = city
        user.save()
        return user
