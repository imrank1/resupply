import os
from resupply import app
from resupply import config
env = os.environ.get('FLASK_ENV', 'development')

port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)



if env =='development':
	app.logger.info("Running in debug mode")
	app.run(debug=True)
else:
	app.run()