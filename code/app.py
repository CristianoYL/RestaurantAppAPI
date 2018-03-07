from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_uploads import configure_uploads, patch_request_class
from security import authenticate, identity
import os
from datetime import timedelta

from resources.user import User, UserUpdate, UserByID
from resources.restaurant import Restaurant, RestaurantByID
from resources.menu import Menu, MenuByID, MenuByRestaurant
from resources.transaction import EphemeralKey
from resources.image import MenuImage

from models.image import MENU_IMAGE_SET

# from resources.order import Order,OrderByID

app = Flask(__name__)

# if running locally, use config file to set environment variables
if __name__ == '__main__':
    import config

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

# To allow flask propagating exception even if debug is set to false on app
app.config['PROPAGATE_EXCEPTIONS'] = True

# Set up flask-uploads configs
app.config['UPLOADED_MENU_DEST'] = os.path.join('static', 'images', 'menu')
patch_request_class(app, 10 * 1024 * 1024)  # restrict max upload image size to 10MB
configure_uploads(app, MENU_IMAGE_SET)

# ================================== endpoints ======================================
jwt = JWT(app, authenticate, identity)  # set up '/auth'

api.add_resource(User, '/user')
api.add_resource(UserUpdate, '/user/password')
api.add_resource(UserByID, '/user/id/<int:userID>')

api.add_resource(Restaurant, '/restaurant')
api.add_resource(RestaurantByID, '/restaurant/id/<int:id>')

api.add_resource(Menu, '/menu')
api.add_resource(MenuByID, '/menu/id/<int:id>')
api.add_resource(MenuByRestaurant, '/menu/restaurant/<int:restaurantID>')

api.add_resource(MenuImage, '/image/menu/<int:menu_id>')

api.add_resource(EphemeralKey, '/transaction/ephemeral_key')

# api.add_resource(Order, '/order')
# api.add_resource(OrderByID, '/order/id/<int:id>')
# ==================================================================================

# will execute this block only if running locally:
if __name__ == '__main__':
    # init db and create tables
    from db import db

    db.init_app(app)


    @app.before_first_request
    def create_tables():
        db.create_all()

    # app.run(host='192.168.1.11', port=8002, debug=True)
    app.run(port=8002, debug=True)
