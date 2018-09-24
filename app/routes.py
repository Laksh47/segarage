from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import requestToolUpload

@app.route('/')
@app.route('/index')

def index():
  return render_template('index.html', greeting="Hw r u")

@app.route('/request_upload', methods=['GET', 'POST'])
def request_upload():
    form = requestToolUpload()
    if form.validate_on_submit():
    	flash('Collected the data {} {}'.format(form.authorname.data, form.papername.data))
    	return redirect(url_for('index'))
    return render_template('request_upload.html', title='Request to upload Tool', form=form)