from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
import os
from datetime import timedelta

from resources.user import User,UserUpdate,UserByID
from resources.restaurant import Restaurant,RestaurantByID
from resources.menu import Menu,MenuByID,MenuByRestaurant
from resources.transaction import EphemeralKey
# from resources.order import Order,OrderByID

app = Flask(__name__)
####################### DB config ####################################
# Heroku DB url/SQlite url
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',config.db_splite_url)

# AWS DB url
# app.config['SQLALCHEMY_DATABASE_URI'] = config.aws_postgresql_url

# Local MySQL url
# app.config['SQLALCHEMY_DATABASE_URI'] = config.local_mysql_url

# get secret and config from os.environ first
app_key = os.environ.get('APP_SECRET_KEY')
db_url = os.environ.get('DATABASE_URL')
if not app_key:
    # if not found, get it from config.py file
    import config
    @app.before_first_request
    def create_tables():
        db.create_all()
    app_key = config.app_secret_key
    db_url = config.db_splite_url
app.secret_key = app_key
app.config['SQLALCHEMY_DATABASE_URI'] = db_url

######################################################################

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

# comment the following section if running on Heroku
###############################
# @app.before_first_request
# def create_tables():
#     db.create_all()
###############################

################ endpoints #############################################
jwt = JWT(app,authenticate,identity)    #set up '/auth'
# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.config['JWT_AUTH_USERNAME_KEY'] = "email"

api.add_resource(User,'/user')
api.add_resource(UserUpdate,'/user/password')
api.add_resource(UserByID,'/user/id/<int:userID>')

api.add_resource(Restaurant,'/restaurant')
api.add_resource(RestaurantByID,'/restaurant/id/<int:id>')

api.add_resource(Menu,'/menu')
api.add_resource(MenuByID,'/menu/id/<int:id>')
api.add_resource(MenuByRestaurant,'/menu/restaurant/<int:rid>')

api.add_resource(EphemeralKey, '/transaction/ephemeral_key')

# api.add_resource(Order, '/order')
# api.add_resource(OrderByID, '/order/id/<int:id>')
######################################################################

if __name__ == '__main__' :
    from db import db
    db.init_app(app)
    app.run(host = '192.168.0.107',port = 5000,debug=True)
