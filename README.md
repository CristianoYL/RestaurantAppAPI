# Introduction
This is a Flask HTTP server, which exposes a set of REST APIs to clients. It provides service for online restaurant ordering. A sample Android app using this service can be found at [my other GitHub repo here.](https://github.com/CristianoYL/RestaurantAndroidApp)
# Configurations
## Environment
The project is developed under ```python-3.6.2```. It is recommended that you use virtual environment to set up the project in case of any version conflicts within your existing installment. One recommendation is to use [virtualenv](https://virtualenv.pypa.io/en/stable/).

You may acquire virtualenv using command:
```
pip install virtualenv
```
You may find futher instructions on virtualenv in the [above link](https://virtualenv.pypa.io/en/stable/).
## Dependencies
This service relies on serveral other services as well. For example, it uses [Flask_JWT](https://pythonhosted.org/Flask-JWT/) for tokenized authentication, [Flask_SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/) for databse interaction, and [Stripe](https://stripe.com/docs) for live credit card charges etc.

A full dependency list could be found in the [requirement.txt file in this repo](https://github.com/CristianoYL/RestaurantAppAPI/blob/master/requirements.txt)

And you may use the Python command to install all the required dependencies easily:
```
pip install -r requirements.txt
```
## Secrets
In order to deploy this service. You'll need to creat a ```config.py``` file in the root folder that includes some secret entries and these values should be kept away from VCS. A sample ```config.py``` file is like this:
```
# stripe secret key to authenticate your service, do not expose it in any VCS
stripe_api_key = <your_stripe_secret_key>

# the private key to encrypt JWT token
app_secret_key = <your_app_secret_key>

# creates a SQLite DB in the root folder for local testing. 
# You may change it to any DB urls of your choice.
# Not required if you deployed your service on Heroku or any other platform,
# on which you must specify a environment variable DATABASE_URL to point to your db url
db_splite_url = "sqlite:///restaurant.db"
```
# Deployment
This project is designed to deploy on Heroku. The [Procfile](https://github.com/CristianoYL/RestaurantAppAPI/blob/master/Procfile) serves as the entry point for Heroku service. And these files are needed only for Heroku deployment:
* Profile
* run.py
* runtime.txt
* uwsgi.ini

Thus if you wish to deploy this service on other platforms or just to test locally, feel free to ignore these files.

However, if you do wish to deploy this service on Heroku, please remember to configure the entries in ```config.py``` as Environment Variables on Heroku in order to let it run.
# API Reference
A detailed API Reference can be found in the [API Reference.md file in this repo](https://github.com/CristianoYL/RestaurantAppAPI/blob/master/API%20Reference.md)
