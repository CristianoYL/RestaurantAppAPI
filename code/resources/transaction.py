from flask_restful import Resource,reqparse
from flask_jwt import jwt_required,current_identity
import traceback, stripe, config

from models.user import UserModel

BLANK_ERROR = '{} cannot be blank'
NOT_FOUND_ERROR: 'User {} not found'
NOT_VALID_ERROR: 'User {} is not valid'
DUPLICATE_ERROR: 'Customer already created'
NULL_CUSTOMER_ERROR: 'Customer not yet created'
INTERNAL_ERROR: 'Internal server error! Failed to {}.'
SUCCESS = 'Customer sucessfully {}'

class EphemeralKey(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('stripe_api_version', type=str, required=True, help=BLANK_ERROR.format('API version'))

    @jwt_required()
    def post(self):
        data = self.parser.parse_args()

        stripe_api_version = data['stripe_api_version']
        customer_id = current_identity.stripeID

        if not customer_id:
            return {'message': NULL_CUSTOMER_ERROR}, 404

        stripe.api_key = config.stripe_api_key
        try:
            ephemeral_key = stripe.EphemeralKey.create(customer=customer_id, api_version=stripe_api_version)
        except:
            traceback.print_exc()
            return {
                    'message' : INTERNAL_ERROR
                        .format("retrieve Stripe Customer info.")
                    },500

        if not ephemeral_key:
            return {'message': NULL_CUSTOMER_ERROR.format('create ephemeral key')}, 404

        return {'ephemeral_key': ephemeral_key}, 200
