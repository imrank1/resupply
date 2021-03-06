from flask.ext.mongoengine import MongoEngine
from resupply.models import *
from flask.ext.mongoengine import DoesNotExist
import ziptax

ziptax.ZIPTAX_API_KEY = 'W38HBWX'

def getSalesTax(zipCode):
	try:
		cachedZipCodeTax = ZipCodeTax.objects.get(zipCode=zipCode)
		return cachedZipCodeTax.taxRate
	except DoesNotExist:
		try:
			tax_rate = 0.06
			#ziptax.get_tax_rate(zipCode)
			newZipCodeTax = ZipCodeTax(zipCode=zipCode,taxRate=tax_rate)
			newZipCodeTax.save()
			return tax_rate
		except ziptax.Ziptax_Failure, e:
			print "FAILED getting zip info DUE TO %s" % e
			return 0.0
