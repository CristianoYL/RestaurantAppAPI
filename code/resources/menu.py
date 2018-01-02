from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
import traceback

from models.menu import MenuModel
from models.restaurant import RestaurantModel

BLANK_ERROR = '{} cannot be blank.'
UNAUTH_ERROR = 'Action unauthorized. Admin previlege required.'
NOT_FOUND_ERROR = 'Menu item <{}> not found.'
ALREADY_EXISTS_ERROR = 'Menu item <{}> already exists for restaurant <{}>.'
INTERNAL_ERROR = 'Internal server error! {}'

class Menu(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('restaurantID', type=int, required=True, help=BLANK_ERROR.format("Restaurant ID"))
    parser.add_argument('name', type=str, required=True, help=BLANK_ERROR.format("Name"))
    parser.add_argument('price', type=float, required=True, help=BLANK_ERROR.format("Price"))
    parser.add_argument('category', type=str, required=True, help=BLANK_ERROR.format("Category"))
    parser.add_argument('description', type=str, required=False)
    parser.add_argument('spicy', type=int, required=False)
    parser.add_argument('isAvailable', type=bool, required=False)
    parser.add_argument('isRecommended', type=bool, required=False)

    @jwt_required()
    def get(self):  # get all menus, for testing only
        user = current_identity
        # TODO: implement admin auth method
        # now assume only user.id = 1 indicates admin
        if user.id != 1:
            return {'message': UNAUTH_ERROR}, 401
        return {'menus': [menu.json() for menu in MenuModel.find_all()]}, 200

    @jwt_required()
    def post(self):  # post a new menu item
        user = current_identity
        # TODO: implement admin auth method
        # now assume only user.id = 1 indicates admin
        if user.id != 1:
            return {'message': UNAUTH_ERROR}, 401

        data = self.parser.parse_args()
        if MenuModel.find_by_name(data['restaurantID'], data['name']):
            return {'message': ALREADY_EXISTS_ERROR.format(data['name'], data['restaurantID'])}, 400

        # set default values if not specified
        if data['spicy'] is None:
            data['spicy'] = 0  # not spicy by default

        if data['isAvailable'] is None:
            data['isAvailable'] = True  # available by default

        if data['isRecommended'] is None:
            data['isRecommended'] = False  # not recommended by default

        menu = MenuModel(None, **data)
        try:
            menu.save_to_db()
        except:
            traceback.print_exc()
            return {'message': INTERNAL_ERROR.format('Failed to create menu item')}, 500
        return menu.json(), 201


class MenuByID(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=False)
    parser.add_argument('price', type=float, required=False)
    parser.add_argument('category', type=str, required=False)
    parser.add_argument('description', type=str, required=False)
    parser.add_argument('spicy', type=int, required=False)
    parser.add_argument('isAvailable', type=bool, required=False)
    parser.add_argument('isRecommended', type=bool, required=False)

    def get(self, id):
        menu = MenuModel.find_by_id(id)
        if menu:
            return menu.json(), 200
        return {'message': NOT_FOUND_ERROR.format(id)}, 404

    @jwt_required()
    def put(self, id):
        user = current_identity
        # TODO: implement admin auth method
        # now assume only user.id = 1 indicates admin
        if user.id != 1:
            return {'message': UNAUTH_ERROR}, 401

        menu = MenuModel.find_by_id(id)
        if not menu:
            return {'message': NOT_FOUND_ERROR.format(id)}, 404

        # update with the given params
        data = self.parser.parse_args()
        if data['name']:
            menu.name = data['name']
        if data['price']:
            menu.price = data['price']
        if data['category']:
            menu.category = data['category']
        if data['description']:
            menu.description = data['description']
        if data['spicy']:
            menu.spicy = data['spicy']
        if data['isAvailable'] is not None:
            menu.isAvailable = data['isAvailable']
        if data['isRecommended'] is not None:
            menu.isRecommended = data['isRecommended']
        try:
            menu.save_to_db()
        except:
            traceback.print_exc()
            return {'message': INTERNAL_ERROR.format('Failed to update menu.')}, 500
        return menu.json(), 200


class MenuByRestaurant(Resource):

    def get(self, restaurantID):
        restaurant = RestaurantModel.find_by_id(restaurantID)
        if restaurant is None:
            return {'message': 'Restaurant <id:{}> not found.'.format(restaurantID)}, 404
        menu_list = [menu.json() for menu in restaurant.menu]
        return {'menus': menu_list}, 200
