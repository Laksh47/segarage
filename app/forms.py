from flask import request
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, MultipleFileField, SelectField
from wtforms.validators import InputRequired, DataRequired, Email, ValidationError

from app.utils import FILETYPE_CHOICES, file_validation

class searchPapers(FlaskForm):
  q = StringField('Search for papers', validators=[DataRequired()])
  search_button = SubmitField('Search papers')

  # def __init__(self, *args, **kwargs):
  #   if 'formdata' not in kwargs:
  #     kwargs['formdata'] = request.args
  #   if 'csrf_enabled' not in kwargs:
  #     kwargs['csrf_enabled'] = False
  #   super(searchPapers, self).__init__(*args, **kwargs)

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

  choices = [(item, item) for item in FILETYPE_CHOICES]
  dropdown_choices = SelectField(choices=choices)
  file_types = StringField()

  all_files = MultipleFileField('Upload your files (readme, binary, script etc.,)', validators=[DataRequired(), InputRequired(), file_validation])

  tags = StringField('Tags', validators=[DataRequired()])

  upload = SubmitField('Upload')