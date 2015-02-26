from datetime import date, timedelta

from flask import abort
from flask.ext.login import UserMixin

from peewee import *
from playhouse.shortcuts import ManyToManyField

from .extensions import db, bcrypt, login_manager


class Base(db.Model):
    @classmethod
    def get_or_404(cls, *query, **kwargs):
        try:
            return cls.get(*query, **kwargs)
        except DoesNotExist:
            abort(404)


@login_manager.user_loader
def load_user(id):
    return User.get(User.id == id)


class Book(Base):
    title = CharField()
    authors = TextField(null=True)
    description = TextField(null=True)
    url = CharField(unique=True)

    def clicks_by_day(self, days=30):
        days = timedelta(days=days)
        date_from = date.today() - days

        click_date = fn.date_trunc('day', Click.clicked_at)
        return Click.select(click_date.alias('click_date'), fn.Count(Click.id).alias('count')). \
            group_by(click_date). \
            where(Click.book == self, click_date >= date_from). \
            order_by(click_date). \
            tuples()

    def to_dict(self):
        return {"id": self.id,
                "title": self.title,
                "authors": self.authors,
                "url": self.url,
                "description": self.description}

    def __repr__(self):
        return "<Book {}>".format(self.title)


class User(Base, UserMixin):
    name = CharField()
    email = CharField(unique=True)
    encrypted_password = CharField(max_length=60)
    favorite_books = ManyToManyField(Book)

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


Favorite = User.favorite_books.get_through_model()


class Click(Base):
    book = ForeignKeyField(Book, related_name="clicks")
    clicked_at = DateTimeField()