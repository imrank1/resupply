class PricingService:
	@staticmethod
	def getPackagePrice(planIdentifier):
		r = planIdentifier.split("-",1)
		package = r[0]
		if(package=="resupplyBasic"):
			return 17
		elif(package=="resupplyPremium"):
			return 25
		elif(package=="resupplyBasic2"):
			return 25
		elif(package=="resupplyPremium2"):
			return 33
		elif(package=="resupplyBasic3"):
			return 33
		elif(package=="resupplyPremium3"):
			return 41
		elif(package=="resupplyBasic4"):
			return 41
		elif(package=="resupplyPremium4"):
			return 49


	@staticmethod
	def getDisplayPackage(package):
		print "in getdisplaypackage package received:" + package
		if(package=="resupplyBasic" or package =="resupplyBasic2" or package =="resupplyBasic3" or package =="resupplyBasic4"):
			return "The Basics"
		else:
			return "Premium"

	@staticmethod
	def getHouseHouldSizeFromPackage(package):
		print "package is:" + package
		r = package.split("-",1)
		packageId = r[0] 
		if(packageId == "resupplyBasic" or packageId == "resupplyPremium"):
			return 1
		else:
			return int(r[0][-1])

	@staticmethod
	def getPricingMap(numFamily):
		pricingMap = None
		if numFamily == 1:
			pricingMap = {"familySize":"1","basicResupplyPackageId":"resupplyBasic","basicPrice":17,"basicLaundryAmt":10,"basicDishwasherAmt":10,"basicToothBrushAmt":1,"basicToothPasteAmt":1,"basicFlossAmt":1,"basicTrashAmt":12,
			"premiumResupplyPackageId":"resupplyPremium","premiumPrice":25,"premiumLaundryAmt":10,"premiumDishwasherAmt":10,"premiumToothBrushAmt":1,"premiumToothPasteAmt":1,"premiumFlossAmt":1,"premiumTrashAmt":12}
		elif numFamily == 2:
			pricingMap = {"familySize":"2","basicResupplyPackageId":"resupplyBasic2","basicPrice":25,"basicLaundryAmt":12,"basicDishwasherAmt":10,"basicToothBrushAmt":2,"basicToothPasteAmt":1,"basicFlossAmt":1,"basicTrashAmt":14,
			"premiumResupplyPackageId":"resupplyPremium2","premiumPrice":33,"premiumLaundryAmt":12,"premiumDishwasherAmt":10,"premiumToothBrushAmt":2,"premiumToothPasteAmt":1,"premiumFlossAmt":1,"premiumTrashAmt":14}
		elif numFamily == 3:
			pricingMap = {"familySize":"3","basicResupplyPackageId":"resupplyBasic4","basicPrice":33,"basicLaundryAmt":16,"basicDishwasherAmt":16,"basicToothBrushAmt":3,"basicToothPasteAmt":2,"basicFlossAmt":2,"basicTrashAmt":18,
			"premiumResupplyPackageId":"resupplyPremium4","premiumPrice":41,"premiumLaundryAmt":16,"premiumDishwasherAmt":16,"premiumToothBrushAmt":3,"premiumToothPasteAmt":2,"premiumFlossAmt":2,"premiumTrashAmt":18}
		elif numFamily == 4:
			pricingMap = {"familySize":"4","basicResupplyPackageId":"resupplyBasic4","basicPrice":41,"basicLaundryAmt":18,"basicDishwasherAmt":16,"basicToothBrushAmt":4,"basicToothPasteAmt":3,"basicFlossAmt":2,"basicTrashAmt":18,
			"premiumResupplyPackageId":"resupplyPremium4","premiumPrice":49,"premiumLaundryAmt":18,"premiumDishwasherAmt":16,"premiumToothBrushAmt":4,"premiumToothPasteAmt":3,"premiumFlossAmt":2,"premiumTrashAmt":18}
		return pricingMap




