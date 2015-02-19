from flask import render_template

from . import app
from .models import Book


@app.route("/")
def index():
    books = Book.query.all()
    return render_template("index.html",
                           books=books)