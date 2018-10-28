from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, DataRequired, Email, ValidationError

from app.utils import allowed_file_readme, allowed_file_tool

def txt_file_check(form, field):
  if field.data and not allowed_file_readme(field.data.filename):
    raise ValidationError('Read me file format not supported (supported: txt, pdf, docx)')

def zip_file_check(form, field):
  if field.data and not allowed_file_tool(field.data.filename):
    raise ValidationError('Format not supported (supported: zip, gz, rar)')

class requestToolUpload(FlaskForm):
  authoremail = StringField('Contact author Email', validators=[DataRequired(), Email('Please enter valid email address')])
  papername = StringField('Paper Name', validators=[DataRequired()])
  # password = PasswordField('Password', validators=[DataRequired()])
  # remember_me = BooleanField('Remember Me')
  recaptcha = RecaptchaField()
  request_upload = SubmitField('Need to upload tool for the paper')

class toolUpload(FlaskForm):
  toolname = StringField('Tool name')
  toolformat = StringField('What are you uploading? VM/Binary/..?', validators=[DataRequired()])

  papername = StringField('Paper Name', validators=[DataRequired()])
  authorname = StringField('Author Name')
  authoremail = StringField('Contact author Email', validators=[DataRequired(), Email('Please enter valid email address')])

  linktopdf = StringField('Link to preprint or public pdf version')
  linktoarchive = StringField('Link to archive (ACM/IEEE/peerJ etc.,)', validators=[DataRequired()])
  linktodemo = StringField('Link to Demo/Website, if any')

  bibtex = TextAreaField('BibTex citation code', validators=[DataRequired()])

  readme_file = FileField('Upload Readme/instructions file', validators=[DataRequired(), txt_file_check])
  scripts_file = FileField('Upload scripts/source code zip (optional)', validators=[zip_file_check])
  all_in_one_file = FileField('Upload final version of the tool (zipped)', validators=[DataRequired(), zip_file_check])

  recaptcha = RecaptchaField()
  upload = SubmitField('Upload')