from flask import Flask
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_mail import Mail

from elasticsearch import Elasticsearch

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import boto3

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

mail = Mail(app)

app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config['ELASTICSEARCH_URL'] else None

## API rate limiter, currently set to 60 calls per minute and 3 calls per second
limiter = Limiter(
  app,
  key_func=get_remote_address,
  default_limits=["60 per minute", "3 per second"],
)

# Create an S3 client
s3 = boto3.client(
  's3',
  aws_access_key_id=app.config['S3_KEY'],
  aws_secret_access_key=app.config['S3_SECRET']
)

from app import routes, models, errors