from flask.ext.login import UserMixin

from . import db, bcrypt, login_manager
from sqlalchemy import func


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    authors = db.Column(db.Text)
    description = db.Column(db.Text)
    url = db.Column(db.String(255), nullable=False, unique=True)

    def clicks_by_day(self):
        click_date = func.cast(Click.clicked_at, db.Date)
        return db.session.query(click_date, func.count(Click.id)). \
            group_by(click_date).filter_by(book_id=self.id). \
            order_by(click_date).all()

    def __repr__(self):
        return "<Book {}>".format(self.title)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    encrypted_password = db.Column(db.String(60))

    favorite_books = db.relationship('Book', secondary='favorite')

    def get_password(self):
        return getattr(self, "_password", None)

    def set_password(self, password):
        self._password = password
        self.encrypted_password = bcrypt.generate_password_hash(password)

    password = property(get_password, set_password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.encrypted_password, password)

    def __repr__(self):
        return "<User {}>".format(self.email)


class Click(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    clicked_at = db.Column(db.DateTime)

    book = db.relationship("Book", backref="clicks")


Favorite = db.Table('favorite',
                    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('book_id', db.Integer, db.ForeignKey('book.id')))