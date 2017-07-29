from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt import jwt_required,current_identity
import requests, traceback

from models.user import UserModel

class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('phone', type=str, required=True,help="Phone cannot be blank.")
    parser.add_argument('password', type=str, required=True, help="Password cannot be blank.")

    def get(self):   #view all users
        users = []
        result = UserModel.find_all()
        for user in result:
            users.append({'id':user.id,'phone':user.phone})
        return {'users':users},200

    def post(self):   #register user
        credentials = self.parser.parse_args()

        user = UserModel.find_by_phone(credentials['phone'])
        if user:
            return {
                'message':'Registration failed! An account with phone<{}> already exists.'
                            .format(credentials['phone'])
                    }, 400

        user = UserModel(None,**credentials)

        try:
            user.save_to_db()
        except:
            return { 'message': 'Internal Server Error, registration failed!' }, 500
        return { 'user': user.json() }, 201

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
    parser = reqparse.RequestParser()
    parser.add_argument('password', type=str, required=True, help="Password cannot be blank.")


    def get(self,userID):   # find user by id
        user = UserModel.find_by_id(userID)
        if user:
            return {'user':user.json()},200
        return {'message':'User <id:{}> not found'.format(_id)},404

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
