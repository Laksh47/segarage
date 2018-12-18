from flask_mail import Message
from app import app, mail
from werkzeug.utils import secure_filename

from time import time
import jwt
import os

ALLOWED_EXTENSIONS_FILES = set(['txt', 'pdf', 'md', 'zip', 'tar', 'gz'])
FILETYPE_CHOICES = ['Binary', 'Scripts (Source code)', 'Readme', 'Other']

def allowed_files(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_FILES

def send_email(subject, sender, recipients, text_body, html_body):
  msg = Message(subject, sender=sender, recipients=recipients)
  msg.body = text_body
  msg.html = html_body
  print("in send mail fn")
  mail.send(msg)

def get_email_token(authoremail, papername, expires_in=6000):
  return jwt.encode(
    {'authoremail': authoremail, 'papername': papername, 'exp': time() + expires_in},
    app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

def verify_email_token(token):
  try:
    payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
  except:
    return
  return payload

def save_file(field, paper_id):
  filename = secure_filename(field.filename)
  filepath = app.config['UPLOAD_FOLDER'] + '/{}/'.format(paper_id)

  if not os.path.exists(os.path.dirname(filepath)):
    os.makedirs(os.path.dirname(filepath))

  field.save(filepath + filename)
