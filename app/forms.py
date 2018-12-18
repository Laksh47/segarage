from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, MultipleFileField
from wtforms.validators import InputRequired, DataRequired, Email, ValidationError

from app.utils import allowed_file_readme, allowed_file_tool

def txt_file_check(form, field):
  if field.data and not allowed_file_readme(field.data.filename):
    raise ValidationError('Read me file format not supported (supported: md, txt, pdf, docx)')

def zip_file_check(form, field):
  if field.data and not allowed_file_tool(field.data.filename):
    raise ValidationError('Format not supported (supported: zip, gz, rar)')

class requestToolUpload(FlaskForm):
  authoremail = StringField('Contact author Email', validators=[DataRequired(), Email('Please enter valid email address')])
  papername = StringField('Paper Name', validators=[DataRequired()])

  recaptcha = RecaptchaField()
  request_upload = SubmitField('Need to upload tool for the paper')

class toolUpload(FlaskForm):
  toolname = StringField('Tool name')

  papername = StringField('Paper Title', validators=[DataRequired()])
  authorname = StringField('Contact author Name')
  authoremail = StringField('Contact author Email', validators=[DataRequired(), Email('Please enter valid email address')])

  linktopdf = StringField('Link to publicly available version of the paper')
  linktoarchive = StringField('Link to published version (ACM/IEEE/peerJ etc.,)', validators=[DataRequired()])
  linktotoolwebpage = StringField('Link to tool webpage')
  linktodemo = StringField('Link to demo (youtube)')

  bibtex = TextAreaField('BibTex entry', validators=[DataRequired()])

  # readme_file = FileField('Upload Readme or instructions file', validators=[DataRequired(), txt_file_check])
  # scripts_file = FileField('Upload source code (optional)', validators=[zip_file_check])
  # binary_file = FileField('Upload final version of the tool (binary)', validators=[DataRequired(), zip_file_check])

  all_files = MultipleFileField('Upload your files (readme, binary, script etc.,)', validators=[DataRequired()])

  tags = StringField('Tags', validators=[DataRequired()])

  upload = SubmitField('Upload')