from flask import request
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, MultipleFileField, SelectField, BooleanField
from wtforms.validators import InputRequired, DataRequired, Email, ValidationError

from app.constants import FILETYPE_CHOICES, CATEGORY_LIST
from app.utils import file_validation, file_upload_or_link, accept_specific_links, valid_url_check

class editButton(FlaskForm):
  # recaptcha_for_edit = RecaptchaField()
  submit = SubmitField('Send the email to edit paper')

class endorsePaper(FlaskForm):
  """
  Form for comment section in view paper page
  """
  commenter_email = StringField('Email', validators=[DataRequired(), Email('Please enter valid email address')])
  commenter_name = StringField('Name (optional)')
  comment = TextAreaField('Feedback for the artifacts', validators=[DataRequired()])
  upvote = BooleanField("Upvote this artifact!")
  recaptcha = RecaptchaField()
  submit =  SubmitField('Submit')

class searchPapers(FlaskForm):
  """
  Search form appears in every view page (navbar)
  """
  q = StringField('Search for papers', validators=[DataRequired()])
  search_button = SubmitField('Search papers')

class requestToolUpload(FlaskForm):
  """
  Request for upload form
  """
  authoremail = StringField('Contact author Email', validators=[DataRequired(), Email('Please enter valid email address')])
  papername = StringField('Paper Name', validators=[DataRequired()])

  recaptcha = RecaptchaField()
  request_upload = SubmitField('Need to upload tool for the paper')

class toolUpload(FlaskForm):
  """
  Tool upload form
  """
  toolname = StringField('Tool name')

  papername = StringField('Paper Title', validators=[DataRequired()])
  authorname = StringField('Contact author Name')
  authoremail = StringField('Contact author Email', validators=[DataRequired(), Email('Please enter valid email address')])

  linktopdf = StringField('Link to publicly available version of the paper', validators=[valid_url_check])
  linktoarchive = StringField('Link to published version (ACM/IEEE/peerJ etc.,)', validators=[DataRequired(), valid_url_check])
  linktodemo = StringField('Link to demo (youtube)', validators=[valid_url_check])

  bibtex = TextAreaField('BibTex entry', validators=[DataRequired()])
  description = TextAreaField('A short description on the Paper/Artifact', validators=[DataRequired()])

  choices = [(item, item) for item in FILETYPE_CHOICES]
  dropdown_choices = SelectField(choices=choices)

  choices = [(item, item) for item in CATEGORY_LIST]
  category = SelectField('Paper category', choices=choices, default='Other')

  file_types = StringField()

  linktotoolwebpage = StringField('Link to tool download', validators=[accept_specific_links])
  all_files = MultipleFileField('Upload your files (readme, binary, script etc.,)', validators=[file_upload_or_link, file_validation])

  tags = StringField('Tags', validators=[DataRequired()])
  
  year = StringField('Year of publication')
  conference = StringField('Conference Name')

  useragreement = BooleanField("I agree to the terms of service", validators=[InputRequired()])

  upload = SubmitField('Upload')

class toolUpdate(FlaskForm):
  """
  Tool update form
  """
  toolname = StringField('Tool name')

  papername = StringField('Paper Title', validators=[DataRequired()])
  authorname = StringField('Contact author Name')
  authoremail = StringField('Contact author Email', validators=[DataRequired(), Email('Please enter valid email address')])

  linktopdf = StringField('Link to publicly available version of the paper', validators=[valid_url_check])
  linktoarchive = StringField('Link to published version (ACM/IEEE/peerJ etc.,)', validators=[DataRequired(), valid_url_check])
  linktodemo = StringField('Link to demo (youtube)', validators=[valid_url_check])

  bibtex = TextAreaField('BibTex entry', validators=[DataRequired()])
  description = TextAreaField('A short description on the Paper/Artifact', validators=[DataRequired()])

  tags = StringField('Tags', validators=[DataRequired()])

  year = StringField('Year of publication')
  conference = StringField('Conference Name')

  files = TextAreaField('Exisiting files', render_kw={'disabled': 'true'}) ## Displaying already uploaded files

  choices = [(item, item) for item in FILETYPE_CHOICES]
  dropdown_choices = SelectField(choices=choices)
  file_types = StringField()

  choices = [(item, item) for item in CATEGORY_LIST]
  category = SelectField('Paper category', choices=choices)

  linktotoolwebpage = StringField('Link to tool download', validators=[accept_specific_links])
  all_files = MultipleFileField('You can either add files or overwrite the existing files by using the same filename!', validators=[file_validation])

  update = SubmitField('Update information')