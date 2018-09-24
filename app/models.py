from app import db

class Paper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    authorname = db.Column(db.String(64))
    papername = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<Paper {}>'.format(self.papername)