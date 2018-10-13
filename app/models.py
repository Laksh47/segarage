from app import db

class Paper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(64))
    paper_name = db.Column(db.Text)
    author_email = db.Column(db.String(120))
    tool_name = db.Column(db.String(200))
    tool_format = db.Column(db.String(64))
    link_to_pdf = db.Column(db.String(250))
    link_to_archive = db.Column(db.String(250))
    link_to_demo = db.Column(db.String(250))
    bibtex = db.Column(db.Text)

    file_urls = db.Column(db.Text)

    created_at  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                       onupdate=db.func.current_timestamp())


    def __repr__(self):
        return '<Paper: {}>'.format(self.paper_name)