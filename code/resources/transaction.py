from flask_restful import Resource,reqparse
from flask_jwt import jwt_required,current_identity
import traceback, stripe

from models.user import UserModel

stripe.api_key = "sk_test_BQokikJOvBiI2HlWgH4olfQ2"

BLANK_ERROR = '{} cannot be null'
NOT_FOUND_ERROR: 'User {} not found'
NOT_VALID_ERROR: 'User {} is not valid'
DUPLICATE_ERROR: 'Customer already created'
NULL_CUSTOMER_ERROR: 'Customer not yet created'
INTERNAL_ERROR: 'Internal server error! Failed to {}.'
SUCCESS = 'Customer sucessfully {}'

class CreateCustomer(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('uid', type=int, required=True, help=BLANK_ERROR.format('User ID'))
    parser.add_argument('token', type=str, required=True, help=BLANK_ERROR.format('Token'))

    def post(self):
        data = self.parser.parse_args()
        user = UserModel.find_by_id(data['uid'])

        if not user:
            return {'message' : NOT_FOUND_ERROR.format(data['uid'])}, 404

        if user.stripe_id:
            return {'message' : DUPLICATE_ERROR}, 402

        if not user.email:
            return {'message' : NOT_VALID_ERROR.format('email')}, 404

        token = data['token']

        try:
            customer = stripe.Customer.create(
                email = user.email,
                source = token,
            )
        except:
            traceback.print_exc()
            return {'message' : INTERNAL_ERROR.format('create a new customer')}, 500

        user.stripe_id = customer.id
        try:
            user.save_to_db()
        except:
            traceback.print_exc()
            return {'message': INTERNAL_ERROR.format('save the new customer to database')}, 500

        return {'message':SUCCESS.format('created')}, 200

class ChargeCustomer(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('amount', type=str, required=True, help=BLANK_ERROR.format('Amount'))

    @jwt_required()
    def post(self):
        data = self.parser.parse_args()
        user = current_identity

        if not user.stripe_id:
            return {'message' : NULL_CUSTOMER_ERROR}, 404
        try:
            stripe.Charge.create(
                amount=data['amount'],
                currency="usd",
                customer=user.stripe_id,
            );
        except:
            traceback.print_exc();
            return {'message': INTERNAL_ERROR.format('charge')}, 500

        return {'message':SUCCESS.format('charged')}, 200

class OneTimeCharge(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('amount', type=int, required=True, help=BLANK_ERROR.format('Amount'))
    parser.add_argument('token', type=str, required=True, help=BLANK_ERROR.format('Token'))

    @jwt_required()
    def post(self):
        data = self.parser.parse_args()
        user = current_identity

        try:
            stripe.Charge.create(
                amount=data['amount'],
                currency="usd",
                source = data['token'],
            );
        except:
            traceback.print_exc();
            return {'message': INTERNAL_ERROR.format('charge')}, 500

        return {'message':SUCCESS.format(user.id)}, 200
