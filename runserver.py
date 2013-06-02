import os
from resupply import app
env = os.environ.get('FLASK_ENV', 'development')

port = int(os.environ.get('PORT', 5000))
if env =="production":
	app.run(debug=False,host='0.0.0.0', port=port)
else:
	app.run(debug=True,host='0.0.0.0', port=port)


