class PricingService:
	@staticmethod
	def getPackagePrice(package):
		if(package=="resupplyBasic"):
			return 17
		elif(package=="resupplyBasicPlus"):
			return 20
		elif(package=="resupplyPremium"):
			return 25
		elif (package=="resupplyPremiumPlus"):
			return 28

	@staticmethod
	def getDisplayPackage(package):
		if(package=="resupplyBasic"):
			return "The Basics"
		elif(package=="resupplyBasicPlus"):
			return "Basic Plus"
		elif(package=="resupplyPremium"):
			return "Premium"
		elif(package =="resupplyPremiumPlus"):
			return "Premium Plus"
