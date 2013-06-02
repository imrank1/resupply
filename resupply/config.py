dev = {
  'stripe_secret_key': 'sk_test_ijEvoQ020mouKyngGA4Bpbfs',
  'stripe_publishable_key': 'pk_test_vQmzWScvJSkMeswQg4Ocu9At',
  'mongodb_db': 'resupply_dev',
  'mongodb_username': 'resupply-dev-fh',
  'mongodb_password': 'fh',
  'mongodb_host': 'alex.mongohq.com',
  'mongodb_port': 10038,
  'mongodb_db':'resupply-dev-fh',
  'secret_key':'cyrus',
  'passwordResetPrefix':'http://localhost:5000/passwordChange/',
  'checkoutRedirect':'https://resupply-production.heroku.com/finalStep'
}

production = {
	'stripe_secret_key': 'sk_live_gwLyLbQojheEPMBHNnzCszTK',
	'stripe_publishable_key': 'pk_live_ypnTkaIKSdMcvvP3Pn3vs2LF',
	'mongodb_db': 'resupply_dev',
	'mongodb_username': 'resupply_dev',
	'mongodb_password': 'imran',
	'mongodb_host': 'alex.mongohq.com',
	'mongodb_port': 10046,
	'secret_key': 'p0c0n0$CyrusImranOnlySirah',
	'passwordResetPrefix':'http://resupply-production.heroku.com/passwordChange/',
  'checkoutRedirect':'localhost:500/finalStep'
}
