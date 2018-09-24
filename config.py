import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'haha segarage secangku'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql://root:root@129.97.171.138/segarage'

    #mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>

    SQLALCHEMY_TRACK_MODIFICATIONS = False