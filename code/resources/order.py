from flask_restful import Resource,reqparse
import traceback

# TODO: order model
from models.order import OrderModel

# Global Variables
BLANK_ERROR = '{} cannot be null'
NOT_FOUND_ERROR: 'Order {} not found'
DUPLICATE_ERROR: 'Duplicate order ID'
INTERNAL_ERROR: 'Internal server error! Failed to create new order.'

class GetOrder(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('oid', type=int, required=True, help = BLANK_ERROR.format('Order ID'))

    def get(self):
        data = self.parser.parse_args()

        this_order = OrderModel.find_by_id(data['oid'])
        if not this_order:
            return {'message' : NOT_FOUND_ERROR.format(data['oid'])}, 404

        return this_order.json(), 200

Class PostOrder(Resource):
    parser = reqparse.RequestParser()
    # parser.add_argument('oid', type=int, required=True, help = BLANK_ERROR.format('Order ID'))
    parser.add_argument('uid', type=int, required=True, help = BLANK_ERROR.format('User ID'))
    parser.add_argument('originalAmount', type=int, required=True, help = BLANK_ERROR.format('Original Amount'))
    parser.add_argument('finalAmount', type=int, required=True, help = BLANK_ERROR.format('Final Amount'))

    # TODO relational way to save menu-id-list
    parser.add_argument('midList', type=list, required=True, location = 'json', help = BLANK_ERROR.format('Menu List'))

    # PENDING, PAID, FULFILLED etc
    parser.add_argument('status', type=str, required=True, help = BLANK_ERROR.format('Status'))

    # TODO type of 'time' & phone
    parser.add_argument('time', type=str, required=True, help = BLANK_ERROR.format('Time'))
    parser.add_argument('phone', type=str, required=True, help = BLANK_ERROR.format('phone'))
    parser.add_argument('deliverAddress', type=str, required=True, help = BLANK_ERROR.format('Deliver Address'))

    def post(self):
        data = self.parser.parse_args()

        if OrderModel.find_by_id(data['oid']):
            return {'message' : DUPLICATE_ERROR}, 400

        # TODO exclude some data
        new_order = OrderModel(None, **data)

        for

        try:
            new_order.save_to_db()
        except:
            traceback.print_exc()
            return {'message': INTERNAL_ERROR},500
        return order.json(),201
