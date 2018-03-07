from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, IMAGES
import os

MENU_IMAGE_SET = UploadSet('menu', IMAGES)
MENU_IMAGE_PREFIX = 'menu_{}'


class MenuImageModel:
    """
    This model servers as a helper to deal with menu image storage.
    All menu images are stored under ./static/images/menu/
    And each menu image is named as menu_{menu_id}.{format}
    """

    def __init__(self, menu_id):
        self.image_name = MENU_IMAGE_PREFIX.format(menu_id)

    @classmethod
    def is_filename_safe(cls, filename):
        """
        check if the filename is safe
        :param filename: name of the file to upload
        :return: True if the filename is safe, False otherwise
        """
        return filename == secure_filename(filename)

    @classmethod
    def get_extension(cls, filename):
        """
        return file's extension, for example
        get_extension('image.jpg') returns '.jpg'
        """
        return os.path.splitext(filename)[1]

    @classmethod
    def get_basename(cls, filename):
        """
        return file's basename, for example
        get_basename('some/folder/image.jpg') returns 'image.jpg'
        """
        # split into (directory, basename)
        return os.path.split(filename)[1]

    @classmethod
    def get_image_path(cls, filename):
        return MENU_IMAGE_SET.path(filename)

    def find_image_for_menu(self):
        """
        Check if the image for this menu item exists
        Note that in this project, we have to check for every allowed image format with the same file basename
        :return: if an image for this menu item exists, return the filename of that image (such as menu_1.jpg)
            if it doesn't exist, return None
        """
        name = self.image_name
        for image_format in IMAGES:  # try the name with every allowed extensions
            filename = self.get_image_path(f'{name}.{image_format}')
            if os.path.isfile(filename):
                return filename
        return None

    def save_to_disk(self, image):
        filename = f'{self.image_name}{self.get_extension(image.filename)}'
        return MENU_IMAGE_SET.save(image, name=filename)

    def delete_from_disk(self, filename):
        """
        this method will check if it's deleting the proper file (the image for the current menu)
        if not, it will raise an IOError.
        :param filename: the name of the file to be deleted
        :return: None
        """
        filename = self.get_basename(filename)  # only compare the basename without extension
        if self.image_name == os.path.splitext(filename)[0]:
            os.remove(self.get_image_path(filename))
        else:
            raise IOError('Filename incorrect, please only delete the current menu image.')
