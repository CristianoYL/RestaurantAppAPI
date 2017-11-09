from flask_restful import Resource, reqparse
import traceback

from models.restaurant import RestaurantModel

class Restaurant(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',type=str,required=True,help='Name cannot be null.')
    parser.add_argument('fee',type=float,required=True,help='Fee cannot be null.')
    parser.add_argument('limit',type=float,required=True,help='Limit cannot be null.')
    parser.add_argument('address',type=str,required=True,help='Address cannot be null.')
    parser.add_argument('openTime',type=str,required=True,help='Open time cannot be null.')
    parser.add_argument('closeTime',type=str,required=True,help='Close time cannot be null.')
    parser.add_argument('isOpen',type=bool,required=False)
    parser.add_argument('logo',type=str,required=False)
    parser.add_argument('promo',type=str,required=False)
    parser.add_argument('phone',type=str,required=True,help='Telephone number cannot be null.')

    def get(self):  # get all restaurants
        return {'restaurants':[res.json() for res in RestaurantModel.find_all()]},200

    def post(self): # create a new restaurant
        data = self.parser.parse_args()
        if RestaurantModel.find_by_name(data['name']):
            return {'message': 'Restaurant {} already exists.'.format(data['name'])}, 400
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
            return {'message': 'Internal server error! Failed to create restaurant.'},500
        return res.json(),201
