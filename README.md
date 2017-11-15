# Introduction
This is a Flask Http server, which exposes a set of REST APIs to users. It provides service for online restaurant ordering. A sample Android app using this service can be found at [my other GitHub repo here.](https://github.com/CristianoYL/RestaurantAndroidApp)
# Configurations
## Dependencies
This service relies on serveral other services as well. For example, it uses ```Flask_JWT``` for tokenized authentication, ```Flask_SQLAlchemy``` for databse interaction, and ```Stripe``` for live credit card charges etc.

A full dependency list could be found in the [requirement.txt file in this repo](https://github.com/CristianoYL/RestaurantAppAPI/blob/master/requirements.txt)
And you may use the Python command to install all the required dependencies easily:
```
pip install -r requirements.txt
```
## Secrets
In order to deploy this service. You'll need to creat a ```config.py``` file in the root folder that includes these secret entries:
```
stripe_secret_key = <stripe secret key>
```

# API Reference
A detailed API Reference can be found in the [API Reference.md file in this repo](https://github.com/CristianoYL/RestaurantAppAPI/blob/master/API%20Reference.md)
