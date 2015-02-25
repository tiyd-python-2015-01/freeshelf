from datetime import datetime
from io import BytesIO

from flask import Blueprint, render_template, flash, redirect, url_for, send_file
from flask.ext.login import login_required, current_user
import matplotlib.pyplot as plt

from ..extensions import db
from ..forms import BookForm
from ..models import Book, Click


books = Blueprint("books", __name__)


@books.route("/")
def index():
    books = Book.query.all()
    return render_template("index.html", books=books)


@books.route("/book/new", methods=["GET", "POST"])
@login_required
def new_book():
    form = BookForm()
    if form.validate_on_submit():
        book = Book.query.filter_by(url=form.url.data).first()
        if book:
            flash("A book with that URL already exists.")
        else:
            book = Book(**form.data)
            db.session.add(book)
            db.session.commit()
            flash("Your book has been added.")
            return redirect(url_for("books.index"))

    return render_template("book_form.html",
                           form=form,
                           post_url=url_for("books.new_book"),
                           button="Add book")


@books.route("/book/<int:id>")
def goto_book(id):
    book = Book.query.get_or_404(id)
    click = Click(book=book, clicked_at=datetime.now())
    db.session.add(click)
    db.session.commit()
    return redirect(book.url, code=301)


@books.route("/book/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_book(id):
    book = Book.query.get(id)
    form = BookForm(obj=book)
    if form.validate_on_submit():
        form.populate_obj(book)
        db.session.commit()
        flash("The book has been updated.")
        return redirect(url_for("books.index"))

    return render_template("book_form.html",
                           form=form,
                           post_url=url_for("books.edit_book", id=book.id),
                           button="Update book")


@books.route("/book/<int:id>/favorite", methods=["POST"])
@login_required
def add_favorite(id):
    book = Book.query.get(id)
    current_user.favorite_books.append(book)
    db.session.commit()
    flash("You have added {} as a favorite.".format(book.title))
    return redirect(url_for("books.index"))


@books.route("/book/<int:id>/data")
def book_data(id):
    book = Book.query.get_or_404(id)
    return render_template("book_data.html",
                           book=book)


def make_clicks_chart(book):
    click_data = book.clicks_by_day()
    dates = [c[0] for c in click_data]
    date_labels = [d.strftime("%b %d") for d in dates]
    every_other_date_label = [d if i % 2 else "" for i, d in enumerate(date_labels)]
    num_clicks = [c[1] for c in click_data]

    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    plt.title("Clicks by day")
    plt.plot_date(x=dates, y=num_clicks, fmt="-")
    plt.xticks(dates, every_other_date_label, rotation=45, size="x-small")
    plt.tight_layout()


@books.route("/book/<int:id>_clicks.png")
def book_clicks_chart(id):
    book = Book.query.get_or_404(id)
    make_clicks_chart(book)

    fig = BytesIO()
    plt.savefig(fig)
    plt.clf()
    fig.seek(0)
    return send_file(fig, mimetype="image/png")


