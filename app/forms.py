from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class requestToolUpload(FlaskForm):
    authorname = StringField('Author Name:', validators=[DataRequired()])
    papername = StringField('Paper Name:', validators=[DataRequired()])
    # password = PasswordField('Password', validators=[DataRequired()])
    # remember_me = BooleanField('Remember Me')
    request_upload = SubmitField('Need to upload tool for the paper')