resupply
========

#### Install pip & dependencies
1. `curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py`
2. `sudo python get-pip.py`
3. `sudo pip install -r requirements.txt


#### Update the configuration settings #####
You will have to set your own mongo, stripe accounts. 

#### Start server
1. Settings for environments are in `config.py`
2. `python runserver.py`

#### Deployment
1. [Install Heroku Toolbelt](https://toolbelt.heroku.com/)
2. `heroku login`
3. `git remote add heroku git@heroku.com:resupply-production.git`
4. `git push heroku master`

