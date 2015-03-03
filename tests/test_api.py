from base64 import b64encode

from flask import json


def basic_auth(username, password):
    return "Basic {}".format(b64encode("{}:{}".format(username, password).encode("utf-8")).decode("utf-8"))


def test_get_book_list(client, book):
    response = client.get("/api/v1/books")
    book_list = json.loads(response.data)
    book_data = book_list["books"][0]
    assert book_data["title"] == book.title
    assert book_data["url"] == book.url


def test_get_book(client, book):
    response = client.get("/api/v1/books/" + str(book.id))
    book_data = json.loads(response.data)
    assert book_data["title"] == book.title
    assert book_data["url"] == book.url


def test_post_book_list(client, user):
    response = client.post(
        "/api/v1/books",
        data=json.dumps({"title": "A New Book", "url": "http://anewbook.org"}),
        content_type="application/json",
        headers={"Authorization": basic_auth(user.email, user.password)})

    new_book = response.json

    assert response.status_code == 201
    assert new_book['id'] is not None
    assert new_book['title'] == "A New Book"


def test_put_book(client, book, user):
    response = client.put(
        "/api/v1/books/" + str(book.id),
        data=json.dumps({"title": "A New Book", "url": "http://anewbook.org"}),
        content_type="application/json",
        headers={"Authorization": basic_auth(user.email, user.password)})

    new_book = response.json

    assert response.status_code == 200
    assert new_book['id'] is book.id
    assert new_book['title'] == "A New Book"


def test_delete_book(client):
    pass

