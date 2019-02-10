import os
import unittest
 
from config import basedir
from app import app, db, mail
from app.models import Paper

# Run command `nose2 -v tests` to run the unit tests
# Run command `coverage run tests.py` to run unittest and measure code coverage!
# Run command `coverage html app/*.py` to get code coverage report!

class TestCase(unittest.TestCase):
  def setUp(self):
    """
    initial unit testing setup
    disabling WTF_CSRF for form submission requests
    test db creation
    """
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')

    self.app = app.test_client()
    db.create_all()

    # Disable send email functionality for unit testing
    mail.init_app(app)
    self.assertEqual(app.debug, False)

  def tearDown(self):
    """
    Destroying the test session
    """
    db.session.remove()
    db.drop_all()


  def test_main_page(self):
    """
    Testing the index page
    """
    response = self.app.get('/', follow_redirects=True)
    self.assertEqual(response.status_code, 200)

  def test_request_upload(self):
    """
    Testing the request upload route function
    parameters => request_upload_form params: author email and paper name
    """
    form_data = { 'authoremail': 'scrawler16.1@gmail.com', 'papername': 'Test paper' }
    response = self.app.post('/request_upload', content_type='multipart/form-data', data=form_data, follow_redirects=True)
    # print(response.__dict__)
    self.assertEqual(response.status, "200 OK")

  def test_search_papers_post(self):
    """
    Searching papers (elastic search test case) body params
    """
    search_form_data = { 'q': 's3' }
    response = self.app.post('/search', content_type='multipart/form-data', data=search_form_data, follow_redirects=True)
    # print(response.__dict__)
    self.assertEqual(response.status, "200 OK")

  def test_search_papers_get(self):
    """
    Searching papers (elastic search test case) query params
    """
    response = self.app.get('/search?q=s3', follow_redirects=True)
    # print(response.__dict__)
    self.assertEqual(response.status, "200 OK")  

  def test_search_papers_fail(self):
    """
    Search when query is None
    """
    response = self.app.get('/search?q=', follow_redirects=True)
    self.assertEqual(response.status, "404 NOT FOUND")

  def test_upload_tool(self):
    """
    Actual upload paper functionality
    """
    

if __name__ == '__main__':
  unittest.main()