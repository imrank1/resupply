import os
from resupply import app
from resupply import config
port = int(os.environ.get('PORT', 5000))
#app.run(debug=True,host='0.0.0.0', port=port)

env = os.environ.get('FLASK_ENV', 'development')

#app.run(host='0.0.0.0', port=port)



if env =='development':
	print 'running in debug mode'
	app.run(debug=True,host='0.0.0.0', port=port)
else:
	app.run()