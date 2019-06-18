import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'mysql://root:@localhost/segarage'

  SQLALCHEMY_TRACK_MODIFICATIONS = False

  #SECURITY_EMAIL_SENDER = ''
  MAIL_SERVER = os.environ.get('MAIL_SERVER')
  MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
  MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
  MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'SE Garage'
  MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
  ADMIN = 'segarage.uwaterloo@gmail.com'

  SECRET_KEY = os.environ.get('SECRET_KEY') or 'SEGarage SECangku'

  RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
  RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')

  # Limit for file uploads set to 25 GB
  MAX_CONTENT_LENGTH = 25 * 1024 * 1024 * 1024
  # MAX_CONTENT_LENGTH = 30 * 1024

  PRESERVE_CONTEXT_ON_EXCEPTION = True
  PROPAGATE_EXCEPTIONS = True

  PER_PAGE = 50

  ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

  PERMANENT_SESSION_LIFETIME =  timedelta(days=1) ## For Flask session cookies

  S3_BUCKET  = os.environ.get("S3_BUCKET_NAME")
  S3_KEY = os.environ.get("S3_ACCESS_KEY")
  S3_SECRET = os.environ.get("S3_SECRET_ACCESS_KEY")
  S3_ENDPOINT = os.environ.get("S3_ENDPOINT")