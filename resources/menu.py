from flask_restful import Resource,reqparse
import traceback

from models.menu import MenuModel

class Menu(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('rid', type=int, required=True,help="Restaurant ID cannot be blank.")
    parser.add_argument('name', type=str, required=True,help="Name cannot be blank.")
    parser.add_argument('price', type=float, required=True, help="Price cannot be blank.")
    parser.add_argument('category', type=str, required=True, help="Category cannot be blank.")
    parser.add_argument('description', type=str, required=False)
    parser.add_argument('spicy', type=int, required=False)
    parser.add_argument('isAvailable', type=bool, required=False)
    parser.add_argument('isRecommended', type=bool, required=False)

    def get(self):  # get all menus, for testing only
        return {'menu':[menu.json() for menu in MenuModel.find_all()]},200

    def post(self): # post a new menu item
        data = self.parser.parse_args()
        if MenuModel.find_by_name(data['rid'],data['name']):
            return {'message': 'Menu item <{}> already exists for restaurant <{}>!'.format(data['name'],data['rid'])},400

        # set default values if not specified
        if data['spicy'] is None:
            data['spicy'] = 0 # not spicy by default

        if data['isAvailable'] is None:
            data['isAvailable'] = True # available by default

        if data['isRecommended'] is None:
            data['isRecommended'] = False # not recommended by default

        menu = MenuModel(None,**data)
        try:
            menu.save_to_db()
        except:
            traceback.print_exc()
            return {'message': 'Internal server error, failed to create menu item'},500
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

    def get(self,id):
        menu = MenuModel.find_by_id(id)
        if menu:
            return menu.json(),200
        return {'message':'Menu item {} not found!'.format(id)},404

    def put(self,id):
        menu = MenuModel.find_by_id(id)
        if not menu:
            return {'message':'Menu item {} not found!'.format(id)},404

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
            return {'message':'Internal server error, failed to update menu.'},500
        return menu.json(),200

class MenuByRestaurant(Resource):

    def get(self,rid):
        menu_list = [menu.json() for menu in MenuModel.find_by_restaurant(rid)]
        return {'menus':menu_list},200
