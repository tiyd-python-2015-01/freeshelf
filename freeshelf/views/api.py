from flask import Blueprint, jsonify
from freeshelf.models import Book

api = Blueprint("api", __name__)

@api.route("/books")
def books():
    books = Book.query.all()
    books = [book.to_dict() for book in books]
    return jsonify({"books": books})

@api.route("/books/<int:id>")
def book(id):
    book = Book.query.get_or_404(id)
    return jsonify(book.to_dict())