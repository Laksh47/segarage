from flask_mail import Message
from app import app, mail

from time import time
import jwt

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