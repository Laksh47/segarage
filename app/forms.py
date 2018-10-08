from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class requestToolUpload(FlaskForm):
  authoremail = StringField('Contact author Email:', validators=[DataRequired()])
  papername = StringField('Paper Name:', validators=[DataRequired()])
  # password = PasswordField('Password', validators=[DataRequired()])
  # remember_me = BooleanField('Remember Me')
  request_upload = SubmitField('Need to upload tool for the paper')

class toolUpload(FlaskForm):
  toolname = StringField('Tool name:')
  toolformat = StringField('What are you uploading? SourceCode/Docker/VM/Binary..?', validators=[DataRequired()])

  papername = StringField('Paper Name:', validators=[DataRequired()])
  authorname = StringField('Author Name:')
  authoremail = StringField('Contact author Email:', validators=[DataRequired()])

  linktopdf = StringField('Link to preprint or public pdf version:')
  linktoarchive = StringField('Link to archive (ACM/IEEE/peerJ etc.,):', validators=[DataRequired()])
  linktoreadme = StringField('Link to read me file/instructions:')
  linktodemo = StringField('Link to Demo/Website, if any:')

  bibtex = StringField('BibTex citation code:', validators=[DataRequired()])

  file = FileField()

  upload = SubmitField('Upload')