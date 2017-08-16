from flask_restful import Resource, reqparse
import traceback

from models.test import TestModel

class Test(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',type=str,required=True,help='name cannot be null.')

    def post(self):
        data = self.parser.parse_args()
        test = TestModel(None,**data)
        try:
            test.save_to_db()
        except:
            traceback.print_exc()
            return {'message':'internal server error.'},500
        return test.json(),201
