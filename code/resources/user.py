from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt import jwt_required,current_identity
import os, traceback, stripe, config

from models.user import UserModel

class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True,help="email cannot be blank.")
    parser.add_argument('phone', type=str, required=False)
    parser.add_argument('password', type=str, required=True, help="Password cannot be blank.")

    def get(self):   #view all users
        users = []
        result = UserModel.find_all()
        for user in result:
            users.append({
                'id' : user.id,
                'stripeID' : user.stripeID,
                'phone':user.phone
            })
        return {'users':users},200

    def post(self):   #register user
        credentials = self.parser.parse_args()
        # check if email is registered
        user = UserModel.find_by_email(credentials['email'])
        if user:
            return {'message':'Account <{}> already exists.'
                            .format(credentials['email'])
                    }, 400
        # try to create a stripe Customer
        try:
            stripe.api_key = os.environ.get('STRIPE_SECRET_KEY',config.stripe_api_key)
            stripe_response = stripe.Customer.create(
                description="Customer for {}".format(credentials['email']),
                email=credentials['email']
            )
            # print(stripe_response)
        except:
            return { 'message': 'Error when creating stripe customer.' }, 500

        # use the stripeID and provided credentials to create user
        user = UserModel(None,stripe_response['id'],**credentials)

        try:
            user.save_to_db()
        except:
            return { 'message': 'Internal Server Error, registration failed!' }, 500
        return user.json(), 201

class UserUpdate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('password', type=str, required=True, help="Password cannot be blank.")

    @jwt_required()
    def put(self):   #change password
        user = current_identity
        new_password = self.parser.parse_args()['password']
        if safe_str_cmp(user.password,new_password):    # no change in new password
            return {'message':'You cannot use the same password!'}, 400
        # if password is valid
        user.password = new_password
        try:
            user.save_to_db()
        except:
            return {'message':'Internal Server Error, change password failed!'}, 500
        return {'message':'password updated!'}, 200


class UserByID(Resource):

    def get(self,userID):   # find user by id
        user = UserModel.find_by_id(userID)
        if user:
            return {'user':user.json()},200
        return {'message':'User <id:{}> not found'.format(userID)},404

    def delete(self,userID):
        user = UserModel.find_by_id(userID)
        if not user:
            return {'message':'User <id:{}> not found'.format(userID)},404
        try:
            user.delete_from_db()
        except:
            traceback.print_exc()
            return {
                'message': 'Internal server error, failed to delete user<id:{}>.'
                    .format(userID)
                    },500
        return {'message': 'User deleted!'},200
