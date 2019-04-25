### Script to be executed only in Flask shell to use proper App's ENV variables

from app import app, db, s3
from app.models import Paper, Tag, File
from werkzeug.utils import secure_filename

import pandas as pd

REPO_FOLDER = '/Users/lakshmanan/Downloads'
excel_file = '/Users/lakshmanan/Downloads/SAMPLE_DATA.xlsx'

def add_temp(paper, tags, filenames, db, s3):

  if tags is not None:
    tags = list(set(map(str.strip, tags.split(",")))) ## Stripping whitespaces and making unique list
    print(tags)

    for tag in tags:
      tag_obj = db.session.query(Tag).filter(Tag.tagname==tag).first()
      if tag_obj is None:
        tag_obj = Tag(tagname=tag)
      paper.tags.append(tag_obj)

  db.session.add(paper)
  db.session.flush()

  if filenames is not None:
    new_filenames = []
    fileurls = []

    for filename in filenames.split(","):
      filename = secure_filename(filename)
      new_filenames.append(filename)
      new_filename = '{}/{}'.format(paper.id, filename) # updating the name with paper.id for easy access

      s3_url = "{0}/{1}/{2}".format(app.config['S3_ENDPOINT'], app.config['S3_BUCKET'], new_filename)

      s3.upload_file('{}/{}'.format(REPO_FOLDER, filename), 'segarage_test', new_filename)
      fileurls.append(s3_url)

    for filename, fileurl in zip(new_filenames, fileurls):
      paper.files.append(File(filename=filename, filetype='Other', fileurl=fileurl))

  db.session.flush()
  db.session.commit()


df = pd.read_excel(excel_file, sheet_name='Sheet1') ## Reading the excel file

dfs = df.where((pd.notnull(df)), None) ## Changing nan to None in the dataframe

for i in range(len(dfs)):
  # print(dfs['filenames'][i])
  paper = Paper(paper_name=dfs['title'][i], author_name=dfs['author_name'][i], author_email=dfs['email-primary'][i], tool_name='Not Provided', link_to_pdf=dfs['acm'][i], link_to_archive='Not provided', link_to_tool_webpage=dfs['available(link)'][i], link_to_demo=dfs['video'][i], bibtex=dfs['bibtex'][i], description=dfs['intro'][i], view_count=0, conference=dfs['conference'][i], year=dfs['year'][i])

  taglist_one = dfs['categories-key words'][i] or ''
  taglist_two = dfs['categories-descirption '][i] or ''
  tags = '{}, {}'.format(taglist_one, taglist_two)
  filenames = dfs['filenames'][i]

  add_temp(paper, tags, filenames, db, s3)
  # Paper.reindex();

