from flask import render_template, flash, redirect, url_for
from flask import request, g, jsonify, session
from flask import Response

from flask_paginate import Pagination, get_page_args

from app import app, db, s3
from .forms import requestToolUpload, toolUpload, searchPapers, endorsePaper, editButton, toolUpdate
from .models import Paper, Tag, File, Comment
from .utils import *
from .constants import CATEGORY_LIST, icondict

from sqlalchemy import func, desc
from os import path

from werkzeug.utils import secure_filename

@app.before_request
def before_request():
  g.search_form = searchPapers()

### Index page
@app.route('/')
@app.route('/index')
def index():
  page, per_page, offset = get_page_args(per_page_parameter="PER_PAGE")

  paginated_papers = Paper.query.limit(per_page).offset(offset)

  count = db.session.query(func.count(Paper.id)).scalar()

  pagination = Pagination(page=page, per_page=per_page, total=count, record_name='papers',format_total=True, format_number=True)

  return render_template('500.html', papers=paginated_papers, icondict=icondict)



### Requesting tool upload and uploading artifacts
@app.route('/request_upload', methods=['GET', 'POST'])
def request_upload():
  form = requestToolUpload()
  if form.validate_on_submit():
    payload = { 'authoremail': form.authoremail.data, 'papername': form.papername.data }
    token = get_email_token(payload)

    text_body=render_template('email/link_to_upload.txt', token=token)
    html_body=render_template('email/link_to_upload.html', token=token)

    ### Email sender needs to be changed before deploying
    send_email('Link to upload tool', app.config['ADMIN'], [form.authoremail.data], text_body, html_body)

    flash('Link to upload the tool has been sent to {} for the paper {}'.format(form.authoremail.data, form.papername.data))
    return redirect(url_for('index'))
  return render_template('request_upload.html', title='Request to upload Tool', form=form)

@app.route('/tool_upload/<token>', methods=['GET', 'POST'])
def tool_upload(token):
  """
  tool upload form takes GET and POST methods
  renders the form for GET
  form submission handling for POST
  """
  payload = verify_email_token(token)
  if not payload:
    flash('Link expired or invalid, try again')
    return redirect(url_for('index'))

  form = toolUpload()
  form.authoremail.data = payload['authoremail']
  form.papername.data = payload['papername']

  if form.validate_on_submit():
    paper = Paper(paper_name=form.papername.data, author_name=form.authorname.data, author_email=form.authoremail.data, tool_name=form.toolname.data, link_to_pdf=form.linktopdf.data, link_to_archive=form.linktoarchive.data, link_to_tool_webpage=form.linktotoolwebpage.data, link_to_demo=form.linktodemo.data, bibtex=form.bibtex.data, description=form.description.data, year=form.year.data, conference=form.conference.data, category=form.category.data, view_count=0)

    # print(form.tags.data)

    for tag in form.tags.data.split(","):
      tag_obj = db.session.query(Tag).filter(Tag.tagname==tag.strip()).first()
      if tag_obj is None:
        tag_obj = Tag(tagname=tag.strip())
      paper.tags.append(tag_obj)

    db.session.add(paper)
    db.session.flush()

    filenames = []
    fileurls = []
    filetypes = form.file_types.data.split(',')

    for file in form.all_files.data:
      if not isinstance(file, str):
        filenames.append(secure_filename(file.filename))

        filename = '{}/{}'.format(paper.id, secure_filename(file.filename))
        file.filename = filename # updating the name with paper.id for easy access

        s3_url = "{0}/{1}/{2}".format(app.config['S3_ENDPOINT'], app.config['S3_BUCKET'], filename)

        upload_file_to_s3(s3, file, app.config['S3_BUCKET'])
        fileurls.append(s3_url)

    # print("Uploaded files below for paper: {}".format(paper.id))
    # print(fileurls)

    for filename, fileurl, filetype in zip(filenames, fileurls, filetypes):
      paper.files.append(File(filename=filename, filetype=filetype, fileurl=fileurl))

    db.session.flush()
    db.session.commit()

    flash('Tool submission success!')

    return redirect(url_for('specific_paper', id=paper.id))

  # print(form.errors)
    
  return render_template('tool_upload.html', title="Upload your tool here", form=form)



### Downloading Artifacts from papers
@app.route('/downloads/<id>/<filename>', methods=['GET'])
def downloads(id, filename):
  """
  Download method to fetch the required file from S3 Bucket
  """
  # print("Resource id: {}".format(id))

  paper = Paper.query.get(id)
  if paper == None:
    return render_template('404.html')

  s3_filename = '{}/{}'.format(paper.id, filename)

  try:
    target_file = s3.get_object(Bucket=app.config['S3_BUCKET'], Key=s3_filename)
  except Exception as e:
    print("Something Happened: ", e)
    return render_template('404.html')

  session_download_key = 'downloaded_{}'.format(paper.id)

  ### Updating paper download count based on session this logic might need to be re-designed
  if session_download_key not in session:
    session[session_download_key] = True

    paper.download_count += 1
    db.session.flush()
    db.session.commit()

  response = Response(
    target_file['Body'],
    mimetype=target_file['ResponseMetadata']['HTTPHeaders']['content-type'],
    headers={"Content-Disposition": "attachment;filename={}".format(filename)}
  )
  return response ## File as download attachment



### Browsing through papers and looking up a specific paper
@app.route('/papers', methods=['GET', 'POST'])
def papers():
  
  """
  Lists all the uploaded paper with pagination
  """

  sort_generic = None
  sort_category = None
  paginated_papers = Paper.query

  page, per_page, offset = get_page_args(per_page_parameter="PER_PAGE")

  

  if request.args.get('sort_generic'):
    sort_generic = request.args.get('sort_generic')
    if sort_generic == "author_name" or sort_generic == "paper_name":
      paginated_papers = paginated_papers.order_by(sort_generic)
    else:
      paginated_papers = paginated_papers.order_by(desc(sort_generic))

  if request.args.get('sort_category'):
    sort_category = request.args.get('sort_category')
    if sort_category != 'Any':
      paginated_papers = paginated_papers.filter_by(category=sort_category)

  paginated_papers = paginated_papers.limit(per_page).offset(offset)

  count = db.session.query(func.count(Paper.id)).scalar()

  pagination = Pagination(page=page, per_page=per_page, total=count, record_name='papers',format_total=True, format_number=True, show_single_page=True)

  return render_template('papers.html', papers=paginated_papers, pagination=pagination, per_page=per_page, icondict=icondict, sort_generic=sort_generic, sort_category=sort_category, categories=CATEGORY_LIST)

@app.route('/papers/<id>', methods=['GET', 'POST'])
def specific_paper(id):
  """
  Renders the individual paper given paper id
  """
  paper = Paper.query.get(id)
  if paper == None:
    return render_template('404.html'), 404

  session_view_key = 'visited_{}'.format(paper.id)

  ### Updating paper view count based on session this logic might need to be re-designed
  if session_view_key not in session:
    session[session_view_key] = True

    paper.view_count += 1
    db.session.flush()
    db.session.commit()

  endorse_form = endorsePaper()
  edit_button = editButton()

  query_obj = paper.comments.filter(Comment.verified==1)
  comments = query_obj.all()
  upvotes = query_obj.filter(Comment.upvoted==1).count()

  return render_template('specific_paper.html', paper=paper, form=endorse_form, edit_button=edit_button, tags=tags_obj_to_str(paper.tags, ", "), comments=comments, upvotes=upvotes, icondict=icondict)



@app.route('/papers/<id>/comments', methods=['POST'])
def add_comment(id):
  """
  Adding comments to a specific paper (unverified)
  """
  # print("paper id: {}".format(id))
  endorse_form = endorsePaper()
  if endorse_form.validate_on_submit():
    # print(endorse_form.__dict__)
    # paper = Paper.query.get(id)

    upvoted = 1 if endorse_form.upvote.data else 0
    commenter_name = endorse_form.commenter_name.data if endorse_form.commenter_name.data else 'Anonymous'
    comment = Comment(commenter_name=commenter_name, commenter_email=endorse_form.commenter_email.data, comment=endorse_form.comment.data, upvoted=upvoted, verified=0, paper_id=id)
    db.session.add(comment)
    db.session.flush()

    ## JWT without expiration for comments
    token = get_email_token({ "comment_id": comment.id, "paper_id": id }, expires_in=None)
    text_body=render_template('email/verify_comment.txt', token=token)
    html_body=render_template('email/verify_comment.html', token=token)

    ### Email sender needs to be changed before deploying
    send_email('Verify Artifact Endorsement - SE Garage', app.config['ADMIN'], [endorse_form.commenter_email.data], text_body, html_body)

    db.session.commit()

    return jsonify(data={'message': 'Submission successfully added, waiting for email verification from {}'.format(endorse_form.commenter_email.data)})
  data = {'errors': endorse_form.errors, 'custom_msg': "Bad request for form submission reload the page and try again"}
  return jsonify(data=data), 400

@app.route('/verify_comment/<token>')
def verify_comment(token):
  """
  Verify the specific comment (makes it visible while viewing the papaer)
  """
  payload = verify_email_token(token)
  if not payload:
    flash('Email token corrupted')
    return redirect(url_for('index'))

  # print("Comment id: {}".format(payload['comment_id']))
  paper = Paper.query.get(payload['paper_id'])
  comment = Comment.query.get(payload['comment_id'])

  if comment.verified == 0:
    comment.verified = 1
    db.session.flush()
    db.session.commit()
    flash('Verification for your recent endorsement on the paper {} is successful'.format(paper.paper_name))
  else:
    flash('Verification done already!')

  return redirect(url_for('index'))



@app.route('/search', methods=['GET', 'POST'])
def search():
  """
  Searching the papers and uses pagination to render the results
  Takes query from GET(query params) and POST (body params)
  """
  if request.args.get('q'):
    g.search_form.q.data = request.args.get('q')
  q = g.search_form.q.data if g.search_form.q.data else None

  if q is None:
    return render_template('404.html'), 404

  page = request.args.get('page', 1, type=int)
  per_page = app.config['PER_PAGE']

  paginated_papers, total = Paper.search(q, page, per_page)

  href="search?q={}".format(q) + '&page={0}' ##customizing to include search query parameter
  pagination = Pagination(href=href, page=page, per_page=per_page, total=total, record_name='papers',format_total=True, format_number=True)
  # print(pagination.__dict__)

  return render_template('papers.html', papers=paginated_papers, pagination=pagination, per_page=per_page, categories=CATEGORY_LIST)



@app.route('/request_update/<id>', methods=['POST'])
def request_update(id):
  """
  Editing the paper information: Requesting, accessing, updating, most of the code are from tool_upload 
  but code duplication done for better understanding and for minor suble changes, 
  might need to be refactored
  """
  # print("paper id: {}".format(id))

  edit_button = editButton()

  if edit_button.validate_on_submit():
    paper = Paper.query.get(id)
    contact_email = paper.author_email

    payload = { 'paper_id': id }
    token = get_email_token(payload)
    text_body=render_template('email/link_to_edit.txt', token=token)
    html_body=render_template('email/link_to_edit.html', token=token)

    ### Email sender needs to be changed before deploying
    send_email('Link to update tool/artifact information', app.config['ADMIN'], [contact_email], text_body, html_body)
    flash('Link to edit/update the artifact information is sent to the contact author, check email')

    return redirect(url_for('specific_paper', id=id))

    data = {'errors': edit_button.errors, 'custom_msg': "Bad request for form submission, try again"}
  return jsonify(data=data), 400


@app.route('/update_tool/<token>', methods=['GET'])
def update_tool(token):
  """
  Update tool page, only renders the form
  """
  payload = verify_email_token(token)
  if not payload:
    flash('Link expired, try again')
    return redirect(url_for('index'))

  paper = Paper.query.get(payload['paper_id'])
  form = toolUpdate()

  form.toolname.data = paper.tool_name
  form.papername.data = paper.paper_name
  form.authorname.data = paper.author_name
  form.authoremail.data = paper.author_email
  form.description.data = paper.description
  form.bibtex.data = paper.bibtex
  form.category.data = paper.category
  form.tags.data = tags_obj_to_str(paper.tags, ", ")
  form.linktopdf.data = paper.link_to_pdf
  form.linktodemo.data = paper.link_to_demo
  form.linktotoolwebpage.data = paper.link_to_tool_webpage
  form.linktoarchive.data = paper.link_to_archive
  form.year.data = paper.year
  form.conference.data = paper.conference


  form.files.data = files_to_str(paper.files, "\n")

  return render_template('tool_update.html', title="Update your tool here", form=form)


@app.route('/update_tool/<token>', methods=['POST'])
def update_tool_submit(token):
  """
  Update tool page, takes care of the form submission
  """
  payload = verify_email_token(token)
  if not payload:
    flash('Link expired, try again')
    return redirect(url_for('index'))

  paper = Paper.query.get(payload['paper_id'])
  form = toolUpdate()
  if form.validate_on_submit():
    paper.tool_name = form.toolname.data
    paper.paper_name = form.papername.data
    paper.author_name = form.authorname.data
    paper.author_email = form.authoremail.data
    paper.description = form.description.data
    paper.bibtex = form.bibtex.data
    paper.category = form.category.data
    paper.link_to_pdf = form.linktopdf.data
    paper.link_to_demo = form.linktodemo.data
    paper.link_to_tool_webpage = form.linktotoolwebpage.data
    paper.link_to_archive = form.linktoarchive.data
    paper.year = form.year.data
    paper.conference = form.conference.data

    paper.tags = []

    for tag in form.tags.data.split(","):
      tag_obj = db.session.query(Tag).filter(Tag.tagname==tag.strip()).first()
      if tag_obj is None:
        tag_obj = Tag(tagname=tag.strip())
      paper.tags.append(tag_obj)

    db.session.flush()
    db.session.commit()

    filenames = []
    fileurls = []
    filetypes = form.file_types.data.split(',')

    for file in form.all_files.data:
      if not isinstance(file, str):
        filenames.append(secure_filename(file.filename))

        filename = '{}/{}'.format(paper.id, secure_filename(file.filename))
        file.filename = filename # updating the name with paper.id for easy access

        bucket_location = s3.get_bucket_location(Bucket=app.config['S3_BUCKET'])
        s3_url = "https://s3.{0}.amazonaws.com/{1}/{2}".format(bucket_location['LocationConstraint'], app.config['S3_BUCKET'], filename)

        upload_file_to_s3(s3, file, app.config['S3_BUCKET'])
        fileurls.append(s3_url)

    # print("Uploaded files below for paper: {}".format(paper.id))
    # print(fileurls)

    existing_files = [x.filename for x in paper.files]

    for filename, fileurl, filetype in zip(filenames, fileurls, filetypes):
      if filename not in existing_files:
        paper.files.append(File(filename=filename, filetype=filetype, fileurl=fileurl))

    db.session.flush()
    db.session.commit()

    flash('Tool information update successfully')
    return render_template('index.html')

  return render_template('tool_update.html', title="Update your tool here", form=form)
