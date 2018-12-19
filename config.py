import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'haha segarage secangku'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql://root:@localhost/segarage'

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

    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or '/Users/lakshmanan/Desktop/Repositories/segarage/uploads'


    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')

    # Limit for file uploads set to 25 GB
    MAX_CONTENT_LENGTH = 25 * 1024 * 1024 * 1024
    # MAX_CONTENT_LENGTH = 30 * 1024

    PER_PAGE = 7