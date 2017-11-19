# Introduction
This is a Flask HTTP server, which exposes a set of REST APIs to clients. It provides service for online restaurant ordering. A sample Android app using this service can be found at [my other GitHub repo here.](https://github.com/CristianoYL/RestaurantAndroidApp)
# Configurations
## Environment
The project is developed under ```python-3.6.2```. It is recommended that you use virtual environment to set up the project in case of any version conflicts within your existing installment. One recommendation is to use [virtualenv](https://virtualenv.pypa.io/en/stable/).

You may acquire virtualenv using command:
```
pip install virtualenv
```
You may find further instructions on virtualenv in the [above link](https://virtualenv.pypa.io/en/stable/).
## Dependencies
This service relies on several other services as well. For example, it uses [Flask_JWT](https://pythonhosted.org/Flask-JWT/) for tokenized authentication, [Flask_SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/) for database interaction, and [Stripe](https://stripe.com/docs) for live credit card charges etc.

A full dependency list could be found in the [requirement.txt file in this repo](https://github.com/CristianoYL/RestaurantAppAPI/blob/master/requirements.txt)

And you may use the Python command to install all the required dependencies easily:
```
pip install -r requirements.txt
```
## Secrets
In order to deploy this service. You'll need to create a ```config.py``` file in the root folder that includes some secret entries and these values should be kept away from VCS. A sample ```config.py``` file is like this:
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
## Instructions
This project is designed to deploy on Heroku. The [Procfile](https://github.com/CristianoYL/RestaurantAppAPI/blob/master/Procfile) serves as the entry point for Heroku service. And these files are needed only for Heroku deployment:
* Profile
* run.py
* runtime.txt
* uwsgi.ini

Thus if you wish to deploy this service on other platforms or just to test locally, feel free to ignore these files and use ```app.py``` as your entry point.

However, if you do wish to deploy this service on Heroku, please remember to configure the entries in ```config.py``` as Environment Variables on Heroku in order to let it run.

## About Deployment
### Local Deployment
If you only need to test the project locally, for example to test a new API, you can simply run the ```app.py``` file in your terminal like this:
```
source ./venv/Script/bin/activate
python app.py
```
where ```./venv``` is the folder that contains your virtual environment, assuming you are using ```virtualenv``` as suggested.

Be aware that you might need a few modification in your ```app.py``` file.
For example, in the following line:
```
app.run(host = '<your_ip>',port = 5000,debug=True)
```
make sure you substitute <your_ip> with your real IP. If you use ```localhost```, your server may run, however, if you are sending requests from another device, such as your phone, then your server may never receive it. Thus it is recommended to use your IP within your LAN, which is often of these formats: ```192.168.x.x``` or ```10.x.x.x```.

### Heroku Deployment
Deploying on Heroku is recommended for individual projects or small businesses. Generally, it requires a minimal knowledge on server deployment and configurations, and it can be free. Thus I deployed most of my personal projects here for long term.

You can set up Databases such as PostgreSQL on Heroku easily using their Add-ons, and Heroku will configure it for you and make sure you have access to the database from your server.

However, if you have sufficient knowledge or growing demand on your server, you may find Heroku less capable. And it's time you consider switching to other cloud hosting services such as AWS.
### AWS Deployment
AWS is designed for industrial level products, and might seem less user-friendly for beginners. However, it is one of the most powerful and convenient hosting services so far. It gives you access to all level of configurations and provides reliability and consistency at its best. Here are some of the features you might find helpful:

* You may choose your server's hardware, CPU and Memory for example.
* You may configure Availability Zones, in case you have performance demand across regions or want resilience against server failures.
* You can config Retention Period as well as Backup frequency to minimize your lost.
* You can use Security Groups for access control. And you can even config Virtual Private Cloud(VPC) to make your database isolated from public network.

Also these features become important when you're to launch your project for production.

# Security
This project emphasize on Security from the following aspects:

* Security of Identity
* Security of Payment
* Security of Communication

## Security of Identity
We enforced tokenized authentication of users in this project, which improved security of identity. All users are encrypted into a Json Web Token(JWT) using [Flask_JWT](https://pythonhosted.org/Flask-JWT/). The basic work flow is as below:
* A user is serialized into a JSON object
* The user JSON object is then encrypted using Private Key Encryption to an access token.
* The token, representing a specific user serves as his identity in the client side, and the server side only accept this token for authentication (except for login).
* The token, if received by server, is decrypted, using the private key, to the JSON object that contains the user's info.

In this way, the user's identity is kept encrypted during all API calls thus is safe from eavesdropping.

## Security of Payment
In this project, we minimized our interaction and knowledge on user's payment information. We do not store any card information from the users on our server, thus there's no risk of leaking payment information if our database is under attack.

We achieve this level of security by following [Stripe's Developer Guide](https://stripe.com/docs/quickstart). We manage all our customer's account and payment information on Stripe, who serves as a industry standard for securely managing payment information and live transactions.

Stripe enforces security using Public Key Encryption. We communicate to Stripe using our Stripe Secret Key as well as a Public Key as follows:

* From our client side, Android App from example, the user post a request containing the Public Key, which is universally publishable, to our server.
* When receiving the request and Public Key, our server uses its Secret Key as well as the user's identity to make a request to the Stripe server. If the request is properly decrypted, which means our Secret Key is authentic, the Stripe Server will generate and respond with an Ephemeral Key. And our server will include this Ephemeral Key in our response to our user.
* Once obtained by the user, the Ephemeral Key serves as a temporary Secret Key. The user then talks directly to the Stripe server instead of our own server for the payment information using the Ephemeral Key. Once the user sets/retrieves his payment source (a particular credit card for example), Stripe respond the user with the Source. And the user post the order, along with the Source, to our server.
* After receiving the order and the payment Source from the user, our server talks to Stripe again(using the Secret Key) and charges the specified Source.

Since all payment information is uploaded and retrieved between the user and Stripe, and our server does not intervene any of the process, we do not share any risk of the payment flow.

In short, we never know your payment information, thus we can never give it away.

## Security of Communication
It is true that we never store any of our customer's information, however, we still need to enforce Security Strategies during communication to prevent eavesdropping.

Fortunately, Stripe has already taken care of secure connection using HTTPS on their side, thus the interaction between our users and Stripe is secure.

Now we only need to make sure that the connection between our server and users are secure. Although we never touch the payment information of our users, there is still a risk. For example, we issue Ephemeral Keys to the users and we accept their payment Source. Also these entities do not contain the raw payment info, it still reveal some information that should not be shared with third parties. Thus we have to enforce HTTPS for our server as well.

However, setting up HTTPS is not a trivial task. You'll need to configure SSL for your server to encrypt the message and provide a certificate. Also in order to verify your certificate, your server should obtain the certificate from a public trusted authority, often referred to as Certificate Authority (CA). You can find a detailed tutorial to set up HTTPS for your Flask server [here](https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https).

Good news is, if you are deploying this project on Heroku, setting up SSL can be much easier. You may follow the Heroku SSL Tutorial [here](https://devcenter.heroku.com/articles/ssl).


# API Reference
A detailed API Reference can be found in the [API Reference.md](https://github.com/CristianoYL/RestaurantAppAPI/blob/master/API%20Reference.md) file in the current repo.
