import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
        UPLOAD_FOLDER = '/home/lucas/microblog/app/uploads'
#       ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'heic'}
        ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'odt', 'rtf', 'csv',
                      'png', 'jpg', 'jpeg', 'gif', 'heic', 'bmp', 'tiff', 'tif', 'webp', 'svg', 'raw',
                      'zip', 'tar', 'gz', 'rar', '7z', 'img'}
        MAX_CONTENT_LENGTH = None
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'app.db')
        SQLALCHEMY_TRACK_MODIFICATIONS = False
