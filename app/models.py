from app import db

paper_tag_association = db.Table('paper_to_tags', db.Model.metadata,
    db.Column('paper_id', db.Integer, db.ForeignKey('papers.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)

class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    tagname = db.Column(db.String(140), unique=True, index=True)

class File(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(140), index=True)
    paper_id = db.Column(db.Integer, db.ForeignKey('papers.id'))

class Paper(db.Model):
    __tablename__ = "papers"
    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(64))
    paper_name = db.Column(db.Text)
    author_email = db.Column(db.String(120))
    tool_name = db.Column(db.String(200))
    link_to_pdf = db.Column(db.String(250))
    link_to_archive = db.Column(db.String(250))
    link_to_tool_webpage = db.Column(db.String(250))
    link_to_demo = db.Column(db.String(250))
    bibtex = db.Column(db.Text)

    files = db.relationship("File")
    tags = db.relationship("Tag", secondary=paper_tag_association)

    created_at  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                       onupdate=db.func.current_timestamp())


    def __repr__(self):
        return '<Paper: {}>'.format(self.paper_name)