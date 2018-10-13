import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'haha segarage secangku'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql://root:root@129.97.171.138/segarage'

    #mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #SECURITY_EMAIL_SENDER = ''
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'Test Scrawler'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMIN = 'scrawler16.1@gmail.com'

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'haha segarage secangku'

    UPLOAD_FOLDER = '/home/larumuga/workspace/segarage/uploads'