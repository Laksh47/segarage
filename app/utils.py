from flask_mail import Message
from app import app, mail
from werkzeug.utils import secure_filename

from time import time
import jwt
import os

ALLOWED_EXTENSIONS_FILES = set(['txt', 'pdf', 'md', 'zip', 'tar', 'gz', 'docx', 'xlsx'])
FILETYPE_CHOICES = ['Binary', 'Scripts (Source code)', 'Readme', 'Other']

def allowed_files(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_FILES

def send_email(subject, sender, recipients, text_body, html_body):
  msg = Message(subject, sender=sender, recipients=recipients)
  msg.body = text_body
  msg.html = html_body
  print("in send mail fn")
  mail.send(msg)

def get_email_token(payload, expires_in=6000):
  payload['exp'] = time() + expires_in
  return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

def get_email_token_comment(payload):
  return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

def verify_email_token(token):
  try:
    payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
  except Exception as e:
    print("Something Happened: ", e)
    return
  return payload

def upload_file_to_s3(s3, file, bucket_name, acl="public-read"):
  try:
    s3.upload_fileobj(
      file,
      bucket_name,
      file.filename,
      ExtraArgs={
        "ACL": acl,
        "ContentType": file.content_type
      }
    )
  except Exception as e:
    # This is a catch all exception, edit this part to fit your needs.
    print("Something Happened: ", e)
    return e

def file_validation(form, field):
  if field.data:
    for file in field.data:
      if isinstance(file, str):
        continue
      if not allowed_files(file.filename):
        raise ValidationError('File format not supported (supported: md, txt, pdf, docx, zip, gz, rar)')

def tags_obj_to_str(tags_array, delimiter=" "):
  tags_str = ""
  for tag in tags_array:
    if tags_str != "":
      tags_str += delimiter
    tags_str += tag.tagname
  return tags_str



##### elasticsearch utils

def add_to_index(index, model):
  if not app.elasticsearch:
    return
  payload = {}

  for field in model.__searchable__:
    if field == 'tags':
      payload[field] = tags_obj_to_str(getattr(model, field))
    else:
      payload[field] = getattr(model, field)
    app.elasticsearch.index(index=index, doc_type=index, id=model.id, body=payload)

def remove_from_index(index, model):
  if not app.elasticsearch:
    return
  app.elasticsearch.delete(index=index, doc_type=index, id=model.id)

def query_index(index, query, page, per_page):
  if not app.elasticsearch:
    return [], 0
  search = app.elasticsearch.search(index=index, doc_type=index, body={'query': {'multi_match': {'query': query, 'fields': ['*']}}, 
    'from': (page - 1) * per_page, 'size': per_page})
  ids = [int(hit['_id']) for hit in search['hits']['hits']]
  return ids, search['hits']['total']