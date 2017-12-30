from flask import Flask, request, jsonify
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

# get secret and config from os.environ first
db_url = os.environ.get('DATABASE_URL')
app.secret_key = os.environ.get('APP_SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
# config JWT auth key name to be 'email' instead of default 'username'
# app.config['JWT_AUTH_USERNAME_KEY'] = "email"

################ endpoints #############################################

jwt = JWT(app,authenticate,identity)    #set up '/auth'

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

# will execute this block only if running locally:
if __name__ == '__main__' :
    # init db and create tables
    from db import db
    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    app.run(debug=True)
