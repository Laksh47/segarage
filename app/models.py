from app import db

from app.utils import add_to_index, remove_from_index, query_index

class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_flush(cls, session, flush_context, instances):
        # print("##### before committt ####")
        # print(session.__dict__)
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_flush(cls, session, flush_context):
        # print("##### after committt ####")
        for obj in session._changes['add']:
            # print(obj)
            if isinstance(obj, SearchableMixin):
                # print("in instance of")
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def before_commit(cls, session):
        # print("##### before committt ####")
        # print(session.__dict__)
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        # print("##### after committt ####")
        for obj in session._changes['add']:
            # print(obj)
            if isinstance(obj, SearchableMixin):
                # print("in instance of")
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_flush', SearchableMixin.before_flush)
db.event.listen(db.session, 'after_flush', SearchableMixin.after_flush)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

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
    filetype = db.Column(db.String(50))
    paper_id = db.Column(db.Integer, db.ForeignKey('papers.id'))

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    commenter_email = db.Column(db.String(120))
    commenter_name = db.Column(db.String(120), default="Anonymous", nullable=False)
    comment = db.Column(db.Text)
    upvoted = db.Column(db.Boolean)
    verified = db.Column(db.Boolean, default=0, nullable=False)
    paper_id = db.Column(db.Integer, db.ForeignKey('papers.id'))

class Paper(SearchableMixin, db.Model):
    __tablename__ = "papers"
    __searchable__ = ['paper_name', 'description', 'tool_name', 'tags'] #fields that should be made full-text search ex: ['paper_name']

    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(64))
    paper_name = db.Column(db.Text)
    author_email = db.Column(db.String(120))
    description = db.Column(db.Text)
    visibility = db.Column(db.Boolean, default=1, nullable=False)
    tool_name = db.Column(db.String(200))
    link_to_pdf = db.Column(db.String(250))
    link_to_archive = db.Column(db.String(250))
    link_to_tool_webpage = db.Column(db.String(250))
    link_to_demo = db.Column(db.String(250))
    bibtex = db.Column(db.Text)

    files = db.relationship("File")
    tags = db.relationship("Tag", secondary=paper_tag_association)
    comments = db.relationship("Comment", lazy='dynamic')

    view_count = db.Column(db.Integer, default=0, nullable=False)
    download_count = db.Column(db.Integer, default=0, nullable=False)

    created_at  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                       onupdate=db.func.current_timestamp())


    def __repr__(self):
        return '<Paper: {}>'.format(self.paper_name)