from . import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    url = db.Column(db.String(255), nullable=False, unique=True)

    def __repr__(self):
        return "<Book {}>".format(self.title)