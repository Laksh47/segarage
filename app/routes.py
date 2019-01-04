from flask import render_template, flash, redirect, url_for, send_from_directory, request, g, jsonify
from flask_paginate import Pagination, get_page_parameter, get_page_args

from app import app
from app import db
from app.forms import requestToolUpload, toolUpload, searchPapers, endorsePaper
from app.models import Paper, Tag, File, Comment
from app.utils import *

from sqlalchemy import func

@app.before_request
def before_request():
  g.search_form = searchPapers()



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
    paper = Paper(paper_name=form.papername.data, author_name=form.authorname.data, author_email=form.authoremail.data, tool_name=form.toolname.data, link_to_pdf=form.linktopdf.data, link_to_archive=form.linktoarchive.data, link_to_tool_webpage=form.linktotoolwebpage.data, link_to_demo=form.linktodemo.data, bibtex=form.bibtex.data, description=form.description.data)

    print(form.tags.data)

    for tag in form.tags.data.split(","):
      tag_obj = db.session.query(Tag).filter(Tag.tagname==tag.strip()).first()
      if tag_obj is None:
        tag_obj = Tag(tagname=tag.strip())
      paper.tags.append(tag_obj)

    db.session.add(paper)
    db.session.flush()

    filenames = []
    filetypes = form.file_types.data.split(',')

    for file in form.all_files.data:
      if not isinstance(file, str):
        save_file(file, paper.id)
        filenames.append(secure_filename(file.filename))

    print("Uploaded files below for paper: {}".format(paper.id))
    print(filenames)

    for filename, filetype in zip(filenames, filetypes):
      paper.files.append(File(filename=filename, filetype=filetype))

    db.session.flush()
    db.session.commit()
    flash('Tool submission success {}'.format(paper.id))

    return redirect(url_for('index'))
    
  return render_template('tool_upload.html', title="Upload your tool here", form=form)



@app.route('/downloads/<id>/<filename>', methods=['GET', 'POST'])
def downloads(id, filename):
  print("Resource id: {}".format(id))
  print("Filename: {}".format(filename))
  print("Dir: {}".format(app.config['UPLOAD_FOLDER'] + "/{}".format(id)))
  return send_from_directory(app.config['UPLOAD_FOLDER'] + "/{}".format(id), filename, as_attachment=True)



@app.route('/papers')
def papers():
  search = False

  # papers = Paper.query.all()
  # print('Total number of papers: {}'.format(len(papers)))

  page, per_page, offset = get_page_args(per_page_parameter="PER_PAGE")
  paginated_papers = Paper.query.limit(per_page).offset(offset)

  count = db.session.query(func.count(Paper.id)).scalar()

  pagination = Pagination(page=page, per_page=per_page, total=count, record_name='papers',format_total=True, format_number=True)

  return render_template('papers.html', papers=paginated_papers, pagination=pagination, per_page=per_page)



@app.route('/papers/<id>', methods=['GET'])
def specific_paper(id):
  print("paper id: {}".format(id))
  paper = Paper.query.get(id)
  if paper == None:
    return render_template('404.html')
  endorse_form = endorsePaper()
  return render_template('specific_paper.html', paper=paper, form=endorse_form)



@app.route('/papers/<id>/comments', methods=['POST'])
def add_comment(id):
  print("paper id: {}".format(id))
  paper = Paper.query.get(id)
  endorse_form = endorsePaper()
  if endorse_form.validate_on_submit():
    print(endorse_form.__dict__)
    upvoted = 1 if endorse_form.upvote.data else 0
    comment = Comment(comment_by_email=endorse_form.commenter_email.data, comment=endorse_form.comment.data, upvoted=upvoted, verified=0, paper_id=id)
    db.session.add(comment)
    db.session.flush()

    token = get_email_token_comment({ "comment_id": comment.id, "paper_id": id })
    text_body=render_template('email/verify_comment.txt', token=token)
    html_body=render_template('email/verify_comment.html', token=token)

    send_email('Verify Artifact Endorsement - SE Garage', app.config['ADMIN'], ['scrawler16.1@gmail.com'], text_body, html_body)

    db.session.commit()

    return jsonify(data={'message': 'Submission successfully added, waiting for email verification from {}'.format(endorse_form.commenter_email.data)})
    data = {'errors': endorse_form.errors, 'custom_msg': "Bad request for form submission reload the page and try again"}
  return jsonify(data=data), 400



@app.route('/verify_comment/<token>')
def verify_comment(token):
  payload = verify_email_token(token)
  if not payload:
    flash('Email token corrupted')
    return redirect(url_for('index'))

  print("Comment id: {}".format(payload['comment_id']))
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

  if request.args.get('q'):
    g.search_form.q.data = request.args.get('q')

  q = g.search_form.q.data if g.search_form.q.data else None

  if q is None:
    return render_template('404.html')

  print("query: {}".format(q))

  page = request.args.get('page', 1, type=int)
  per_page = app.config['PER_PAGE']

  paginated_papers, total = Paper.search(q, page, per_page)

  href="search?q={}".format(q) + '&page={0}' ##customizing to include search query parameter
  pagination = Pagination(href=href, page=page, per_page=per_page, total=total, record_name='papers',format_total=True, format_number=True)
  print(pagination.__dict__)

  return render_template('papers.html', papers=paginated_papers, pagination=pagination, per_page=per_page)
