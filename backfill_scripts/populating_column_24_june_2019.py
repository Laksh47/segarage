from app import app, db
from app.models import Paper

import pandas as pd

excel_file = '/Users/lakshmanan/Downloads/april23_clean.xlsx'

def update_paper(paper_name, category):
	if category:
		paper = Paper.query.filter_by(paper_name=paper_name).first()
		paper.category = category
		print(paper)

		db.session.commit()


df = pd.read_excel(excel_file, sheet_name='Sheet1') ## Reading the excel file
dfs = df.where((pd.notnull(df)), None) ## Changing nan to None in the dataframe

for i in range(len(dfs)):
	category_string = dfs['categories-Session name'][i].strip()
	update_paper(dfs['title'][i], category_string)

Paper.reindex();
