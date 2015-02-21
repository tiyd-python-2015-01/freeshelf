#!/usr/bin/env python
import csv
import os

from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand
from flask.ext.script.commands import ShowUrls, Clean

from freeshelf import app, db, models

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

manager = Manager(app)
manager.add_command('server', Server())
manager.add_command('db', MigrateCommand)
manager.add_command('show-urls', ShowUrls())
manager.add_command('clean', Clean())


@manager.shell
def make_shell_context():
    """ Creates a python REPL with several default imports
        in the context of the app
    """

    return dict(app=app, db=db, Book=models.Book, User=models.User)


@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code

@manager.command
def seed():
    """Seed the books with all books in seed_books.csv."""
    books_added = 0
    books_updated = 0
    with open('seed_books.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            book = models.Book.query.filter_by(url=row['url']).first()
            if book is None:
                book = models.Book()
                books_added += 1
            else:
                books_updated += 1
            for key, value in row.items():
                setattr(book, key, value)
            db.session.add(book)
        db.session.commit()
        print("{} books added, {} books updated.".format(books_added, books_updated))



if __name__ == '__main__':
    manager.run()
