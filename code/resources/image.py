from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage
from flask_uploads import UploadNotAllowed
from flask import send_file
from flask_jwt import jwt_required, current_identity
import traceback

from models.image import MenuImageModel
from models.menu import MenuModel

BLANK_ERROR = '{} cannot be blank.'
UNAUTH_ERROR = 'Action unauthorized. Admin privilege required.'
NOT_FOUND_ERROR = '{} not found.'
INTERNAL_ERROR = 'Internal server error! {}'


class MenuImage(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('image',
                        type=FileStorage,
                        location='files',
                        required=True,
                        help=BLANK_ERROR.format('image')
                        )

    @jwt_required()
    def put(self, menu_id):
        """
        This endpoint is used to upload an image for a menu item. If there is already an image
        for that menu item, it will overwrite the existing file.
        """
        data = self.parser.parse_args()

        # user = current_identity
        # TODO: add user privilege check

        menu = MenuModel.find_by_id(menu_id)
        if not menu:
            return {'message': NOT_FOUND_ERROR.format(f'Menu item <id={menu_id}>')}, 404

        menu_image = MenuImageModel(menu_id)
        # check if the image file exists
        filename = menu_image.find_image_for_menu()
        if filename:  # image for this menu already exists
            # delete the existing image first
            try:
                menu_image.delete_from_disk(filename)
            except IOError:
                traceback.print_exc()
                return {'message': INTERNAL_ERROR.format('Failed to update menu image.')}, 500
        try:
            file = menu_image.save_to_disk(data['image'])
            menu.image = menu_image.get_image_path(file)
            menu.save_to_db()
            return {'message': f'Menu image <{file}> saved!'}, 200
        except UploadNotAllowed:  # forbidden file type
            extension = menu_image.get_extension(data['image'].filename)
            return {'message': f'Extension <{extension}> is not allowed.'}, 400
        except:
            traceback.print_exc()
            return {'message': INTERNAL_ERROR.format('Failed to update menu info.')}, 500

    def get(self, menu_id):
        """
        This endpoint returns the requested image if exists. It will use JWT to
        retrieve user information and look for the image inside the user's folder.
        """
        menu_image = MenuImageModel(menu_id)

        filename = menu_image.find_image_for_menu()
        if filename:
            return send_file(filename)
        return {'message': f'Image for menu <id={menu_id}> not found.'}, 404

    @jwt_required()
    def delete(self, menu_id):
        """
        This endpoint is used to delete the requested image under the user's folder.
        It uses the JWT to retrieve user information.
        """
        # user = current_identity
        # TODO: add admin privilege check
        menu_image = MenuImageModel(menu_id)

        filename = menu_image.find_image_for_menu()
        if filename:
            try:
                menu_image.delete_from_disk(filename)
                return {'message': f'Image for menu item <id={menu_id}> deleted!'}, 200
            except IOError:
                traceback.print_exc()
                return {'message': INTERNAL_ERROR.format('Failed to delete menu image.')}, 500
        return {'message': f'Image for menu <id={menu_id}> not found.'}, 404
