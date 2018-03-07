from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt import jwt_required, current_identity
import os, traceback, stripe

from models.user import UserModel
from utils.privilege import is_admin

BLANK_ERROR = '{} cannot be blank.'
UNAUTH_ERROR = 'Action unauthorized. Admin privilege required.'
NOT_FOUND_ERROR = 'User <{}> not found.'
ALREADY_EXISTS_ERROR = 'User <{}> already exists.'
INTERNAL_ERROR = 'Internal server error! {}'


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help=BLANK_ERROR.format("Email"))
    parser.add_argument('phone', type=str, required=False)
    parser.add_argument('password', type=str, required=True, help=BLANK_ERROR.format("Password"))

    @jwt_required()
    def get(self):  # view all users
        if not is_admin(current_identity):
            return {'message': 'Admin privilege not satisfied.'}, 401

        users = []
        result = UserModel.find_all()
        for user in result:
            users.append({
                'id': user.id,
                'stripeID': user.stripeID,
                'email': user.email,
                'phone': user.phone
            })
        return {'users': users}, 200

    def post(self):  # register user
        credentials = self.parser.parse_args()
        # check if email is registered
        user = UserModel.find_by_email(credentials['email'])
        if user:
            return {'message': ALREADY_EXISTS_ERROR
                .format(credentials['email'])
                    }, 400
        # try to create a stripe Customer
        try:
            # get secret from os.environ first
            key = os.environ.get('STRIPE_SECRET_KEY')
            if not key:
                # if not found, get it from config.py file
                import config
                key = config.stripe_api_key
            stripe.api_key = key

            stripe_response = stripe.Customer.create(
                description="Customer for {}".format(credentials['email']),
                email=credentials['email']
            )
            # print(stripe_response)
        except:
            return {'message': 'Error when creating stripe customer.'}, 500

        # use the stripeID and provided credentials to create user
        user = UserModel(None, stripe_response['id'], **credentials)

        try:
            user.save_to_db()
        except:
            return {'message': INTERNAL_ERROR
                .format('Registration failed!')}, 500
        return user.json(), 201


class UserUpdate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('password', type=str, required=True, help=BLANK_ERROR.format("Password"))

    @jwt_required()
    def put(self):  # change password
        user = current_identity
        new_password = self.parser.parse_args()['password']
        if safe_str_cmp(user.password, new_password):  # no change in new password
            return {'message': 'You cannot use the same password!'}, 400
        # if password is valid
        user.password = new_password
        try:
            user.save_to_db()
        except:
            return {'message': INTERNAL_ERROR
                .format('Change password failed!')}, 500
        return {'message': 'password updated!'}, 200


class UserByID(Resource):

    @jwt_required()
    def get(self, userID):  # find user by id
        if not is_admin(current_identity):
            return {'message': 'Admin privilege not satisfied.'}, 401

        user = UserModel.find_by_id(userID)
        if user:
            return {'user': user.json()}, 200
        return {'message': NOT_FOUND_ERROR.format(userID)}, 404

    @jwt_required()
    def delete(self, userID):
        if not is_admin(current_identity):
            return {'message': 'Admin privilege not satisfied.'}, 401

        user = UserModel.find_by_id(userID)
        if not user:
            return {'message': NOT_FOUND_ERROR.format(userID)}, 404
        try:
            user.delete_from_db()
        except:
            traceback.print_exc()
            return {
                       'message': INTERNAL_ERROR.format('Failed to delete user<id:{}>.'
                                                        .format(userID))
                   }, 500
        return {'message': 'User deleted!'}, 200
