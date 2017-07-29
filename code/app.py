import os

from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
# import config

from resources.user import User,UserUpdate,UserByID

app = Flask(__name__)
####################### DB config ####################################
# Heroku DB url/SQlite url
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///restaurant.db')

# AWS DB url
# app.config['SQLALCHEMY_DATABASE_URI'] = config.aws_postgresql_url

# Local MySQL url
# app.config['SQLALCHEMY_DATABASE_URI'] = config.local_mysql_url
######################################################################

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'restaurant_secret_key'
api = Api(app)

# comment the following section if running on Heroku
###############################
@app.before_first_request
def create_tables():
    db.create_all()
###############################

################ endpoints #############################################
jwt = JWT(app,authenticate,identity)    #set up '/auth'

api.add_resource(User,'/user')
api.add_resource(UserUpdate,'/user/password')
api.add_resource(UserByID,'/user/id/<int:userID>')

######################################################################

if __name__ == '__main__' :
    from db import db
    db.init_app(app)
    app.run(host = '192.168.1.9',port = 5000,debug=True)
