from flask import Flask
from flask_mail import Mail, Message
import os

app = Flask(__name__)
mail = Mail(app)
mail_settings = {
  "MAIL_SERVER": 'smtp.gmail.com',
  "MAIL_PORT": 587,
  "MAIL_USE_TLS": True,
  "MAIL_USE_SSL": True,
  "MAIL_USERNAME": 'scrawler16.1@gmail.com',
  "MAIL_PASSWORD": ''
}
app.config.update(mail_settings)


if __name__ == '__main__':
  with app.app_context():
    msg = Message(subject="Hello",sender='scrawler16.1@gmail.com',recipients=['larumuga@uwaterloo.ca'],body="work nowwww!!")
    mail.send(msg)