from flask import Blueprint, url_for, abort, g

from flask.ext.login import current_user

from ..api_helpers import returns_json, APIView, api_form
from ..forms import BookForm
from ..extensions import login_manager, db
from ..models import Book, User


api = Blueprint("api", __name__)


@api.app_errorhandler(401)
@returns_json
def unauthorized(request):
    return {"error": "This API call requires authentication."}, 401


@login_manager.request_loader
def authorize_user(request):
    authorization = request.authorization
    if authorization:
        email = authorization['username']
        password = authorization['password']

        user = User.query.filter_by(email=email).first()
        if user.check_password(password):
            return user

    return None


def require_authorization():
    if not current_user.is_authenticated():
        abort(401)


class BookListView(APIView):
    def get(self):
        books = Book.query.all()
        books = [book.to_dict() for book in books]
        return {"books": books}

    def post(self):
        require_authorization()
        form = api_form(BookForm, data=g.data)
        if form.validate():
            book = Book.query.filter_by(url=form.url.data).first()
            if book:
                return {"url": "This URL has already been taken."}, 400
            else:
                book = Book(**form.data)
                db.session.add(book)
                db.session.commit()
                return book.to_dict(), 201, {"Location": url_for(".book", id=book.id, _external=True)}
        else:
            return form.errors, 400


class BookView(APIView):
    def get(self, id):
        book = Book.query.get_or_404(id)
        return book.to_dict()

    def put(self, id):
        require_authorization()
        book = Book.query.get_or_404(id)
        for key, value in g.data.items():
            setattr(book, key, value)
        form = api_form(BookForm, obj=book)
        if form.validate():
            form.populate_obj(book)
            db.session.commit()
            return book.to_dict(), 200
        else:
            return form.errors, 400


class FavoriteView(APIView):
    def post(self, book_id):
        require_authorization()
        book = Book.query.get_or_404(book_id)
        current_user.favorite_books.append(book)
        db.session.commit()
        return {"book_id": book.id, "favorite": True}, 201



api.add_url_rule('/books', view_func=BookListView.as_view('books'))
api.add_url_rule('/books/<int:id>', view_func=BookView.as_view('book'))
api.add_url_rule('/books/<int:book_id>/favorite', view_func=FavoriteView.as_view('favorite'))
