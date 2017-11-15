# Introduction
This is a Flask Http server, which exposes a set of REST APIs to users. It provides service for online restaurant ordering. A sample Android app using this service can be found at [my other GitHub repo here.](https://github.com/CristianoYL/RestaurantAndroidApp)
# Configurations
## Environment
The project is developed under ```python-3.6.2```. It is recommended that you use virtual environment to set up the project in case of any version conflicts within your existing installment. One recommendation is to use [virtualenv](https://virtualenv.pypa.io/en/stable/).

You may aquire virtualenv using command:
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
stripe_secret_key = <stripe secret key>
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
