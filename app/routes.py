from flask import render_template, flash, redirect, url_for
from app import app
from app import db
from app.forms import requestToolUpload, toolUpload
from app.models import Paper
from app.utils import *
from werkzeug.utils import secure_filename

import os

@app.route('/')
@app.route('/index')

def index():
  return render_template('index.html', greeting="You can upload your tool by clicking the above 'Request Upload' button")

@app.route('/request_upload', methods=['GET', 'POST'])
def request_upload():
  form = requestToolUpload()
  if form.validate_on_submit():
    token = get_email_token(form.authoremail.data, form.papername.data)

    text_body=render_template('email/link_to_upload.txt', token=token)
    html_body=render_template('email/link_to_upload.html', token=token)

    send_email('Link to upload tool', app.config['ADMIN'], ['scrawler16.1@gmail.com'], text_body, html_body)

    flash('Link to upload the tool has been sent to {} for the paper {}'.format(form.authoremail.data, form.papername.data))
    return redirect(url_for('index'))
  return render_template('request_upload.html', title='Request to upload Tool', form=form)



@app.route('/tool_upload/<token>', methods=['GET', 'POST'])
def tool_upload(token):

  payload = verify_email_token(token)
  if not payload:
    return redirect(url_for('index'))

  form = toolUpload()
  form.authoremail.data = payload['authoremail']

  if form.validate_on_submit():
    paper = Paper(paper_name=form.papername.data, author_name=form.authorname.data, author_email=form.authoremail.data, tool_name=form.toolname.data, tool_format=form.toolformat.data, link_to_pdf=form.linktopdf.data, link_to_archive=form.linktoarchive.data, link_to_demo=form.linktodemo.data, bibtex=form.bibtex.data)

    db.session.add(paper)
    db.session.flush()

    filename = secure_filename(form.readme_file.data.filename)
    filepath = app.config['UPLOAD_FOLDER'] + '/{}/'.format(paper.id)

    if not os.path.exists(os.path.dirname(filepath)):
      os.makedirs(os.path.dirname(filepath))

    form.readme_file.data.save(filepath + filename)

    db.session.commit()
    flash('Tool submission success {}'.format(paper.id))

    return redirect(url_for('index'))
    
  return render_template('tool_upload.html', title="Upload your tool here", form=form)