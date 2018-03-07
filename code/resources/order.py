from flask_restful import Resource, reqparse
from datetime import datetime, timezone
from flask_jwt import jwt_required, current_identity
import os, traceback, stripe

# TODO: order model
from models.order import OrderModel

# Global Variables
BLANK_ERROR = '{} cannot be null'
NOT_FOUND_ERROR: 'Order {} not found'
DUPLICATE_ERROR: 'Duplicate order ID'
INTERNAL_ERROR: 'Internal server error! Failed to {}.'
SUCCESS: 'Order {} successfully paid'


# Utils

def update_order_status(order, status):
    order['status'].append({
        'status': status,
        'time': datetime.now(timezone.utc)
    })


class Order(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('order', type=str, required=True, help=BLANK_ERROR.format('Order informaton'))

    @jwt_required()
    def post(self):
        data = self.parser.parse_args()

        customer_id = current_identity.stripeID
        order = data['order']

        update_order_status(order, 'pending')

        try:
            # get secret from os.environ first
            key = os.environ.get('STRIPE_SECRET_KEY')
            if not key:
                # if not found, get it from config.py file
                import config
                key = config.stripe_api_key
            stripe.api_key = key

            this_charge = stripe.Charge.create(
                amount=order['total'],
                source=order['source'],
                currency='usd',
                metadata={
                    'order_id': order['id'],
                }
            )

            update_order_status(order, 'paid')
            order['charge_id']: this_charge

        except:
            traceback.print_exc()
            update_order_status(order, 'failed')

            return {
                       'message': INTERNAL_ERROR.format('create charge')
                   }, 200

        # TODO save to order model

        return {
                   'message': SUCCESS.format(order['id'])
               }, 200


class OrderByID(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('oid', type=int, required=True, help=BLANK_ERROR.format('Order ID'))

    def get(self):
        data = self.parser.parse_args()

        this_order = OrderModel.find_by_id(data['oid'])
        if not this_order:
            return {'message': NOT_FOUND_ERROR.format(data['oid'])}, 404

        return this_order.json(), 200
