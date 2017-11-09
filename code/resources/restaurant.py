from flask_restful import Resource, reqparse
from flask_jwt import jwt_required,current_identity
import traceback

from models.restaurant import RestaurantModel

BLANK_ERROR = '{} cannot be blank.'
NOT_FOUND_ERROR = 'Restaurant {} not found.'
ALREADY_EXISTS_ERROR = 'Restaurant {} already exists.'
INTERNAL_ERROR = 'Internal server error! {}'
UNAUTH_ERROR = 'Action unauthorized. Admin previlege required.'

class Restaurant(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',type=str,required=True,help=BLANK_ERROR.format('Name'))
    parser.add_argument('fee',type=float,required=True,help=BLANK_ERROR.format('Delivery fee'))
    parser.add_argument('limit',type=float,required=True,help=BLANK_ERROR.format('Limit'))
    parser.add_argument('address',type=str,required=True,help=BLANK_ERROR.format('Address'))
    parser.add_argument('openTime',type=str,required=True,help=BLANK_ERROR.format('Open time'))
    parser.add_argument('closeTime',type=str,required=True,help=BLANK_ERROR.format('Close time'))
    parser.add_argument('isOpen',type=bool,required=False)
    parser.add_argument('logo',type=str,required=False)
    parser.add_argument('promo',type=str,required=False)
    parser.add_argument('phone',type=str,required=True,help=BLANK_ERROR.format('Telephone'))

    @jwt_required()
    def get(self):  # get all restaurants
        user = current_identity
        #TODO: implement admin auth method
        # now assume only user.id = 1 indicates admin
        if user.id != 1:
            return {'message': UNAUTH_ERROR},401
        return {'restaurants':[res.json() for res in RestaurantModel.find_all()]},200

    def post(self): # create a new restaurant
        data = self.parser.parse_args()
        if RestaurantModel.find_by_name(data['name']):
            return {'message': ALREADY_EXISTS_ERROR
                .format(data['name'])}, 400
        # else try to create new restaurant
        if data['isOpen'] is None:
            data['isOpen'] = True   # open by default

        # if data['logo'] is None:
        #     data['logo'] = default_logo_url

        res = RestaurantModel(None,**data)
        try:
            res.save_to_db()
        except:
            traceback.print_exc()
            return {'message': INTERNAL_ERROR
                .format('Failed to create restaurant.')},500
        return res.json(),201

class RestaurantByID(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',type=str,required=False)
    parser.add_argument('fee',type=float,required=False)
    parser.add_argument('limit',type=float,required=False)
    parser.add_argument('address',type=str,required=False)
    parser.add_argument('openTime',type=str,required=False)
    parser.add_argument('closeTime',type=str,required=False)
    parser.add_argument('isOpen',type=bool,required=False)
    parser.add_argument('logo',type=str,required=False)
    parser.add_argument('promo',type=str,required=False)
    parser.add_argument('phone',type=str,required=False)

    @jwt_required()
    def put(self,id): # update a restaurant
        user = current_identity
        #TODO: implement admin auth method
        # now assume only user.id = 1 indicates admin
        if user.id != 1:
            return {'message': UNAUTH_ERROR},401

        data = self.parser.parse_args()
        restaurant = RestaurantModel.find_by_id(id)
        if restaurant is None:
            return {'message': NOT_FOUND_ERROR.format(data['name'])}, 404
        # else update with given info restaurant
        if data['name']:
            restaurant.name = data['name']
        if data['fee']:
            restaurant.fee = data['fee']
        if data['limit']:
            restaurant.limit = data['limit']
        if data['address']:
            restaurant.address = data['address']
        if data['openTime']:
            restaurant.openTime = data['openTime']
        if data['closeTime']:
            restaurant.closeTime = data['closeTime']
        if data['isOpen'] is not None:
            restaurant.isOpen = data['isOpen']
        if data['logo']:
            restaurant.logo = data['logo']
        if data['promo']:
            restaurant.promo = data['promo']
        if data['phone']:
            restaurant.phone = data['phone']

        try:
            restaurant.save_to_db()
        except:
            traceback.print_exc()
            return {'message': INTERNAL_ERROR
                .format('Failed to update restaurant.')},500
        return restaurant.json(),200
