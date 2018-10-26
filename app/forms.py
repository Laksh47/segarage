from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class requestToolUpload(FlaskForm):
  authoremail = StringField('Contact author Email:', validators=[DataRequired()])
  papername = StringField('Paper Name:', validators=[DataRequired()])
  # password = PasswordField('Password', validators=[DataRequired()])
  # remember_me = BooleanField('Remember Me')
  request_upload = SubmitField('Need to upload tool for the paper')

class toolUpload(FlaskForm):
  toolname = StringField('Tool name:')
  toolformat = StringField('What are you uploading? VM/Binary/..?', validators=[DataRequired()])

  papername = StringField('Paper Name:', validators=[DataRequired()])
  authorname = StringField('Author Name:')
  authoremail = StringField('Contact author Email:', validators=[DataRequired()])

  linktopdf = StringField('Link to preprint or public pdf version:')
  linktoarchive = StringField('Link to archive (ACM/IEEE/peerJ etc.,):', validators=[DataRequired()])
  linktodemo = StringField('Link to Demo/Website, if any:')

  bibtex = TextAreaField('BibTex citation code:', validators=[DataRequired()])

  readme_file = FileField()
  scripts_file = FileField()
  all_in_one_file = FileField()

  upload = SubmitField('Upload')