class PricingService:
	@staticmethod
	def getPackagePrice(package):
		if(package=="basic"):
			return 17
		elif(package=="basicPlus"):
			return 20
		elif(package=="premium"):
			return 25
		elif (package=="premiumPlus"):
			return 28

