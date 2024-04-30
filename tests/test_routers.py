import pytest
from conftest import client, test_async_session
from models import Author, Book
from sqlalchemy import insert, select


async def test_get_authors(client):
    response = await client.get("/authors/")
    assert response.status_code == 200
    authors = response.json()
    assert isinstance(authors, list)


async def test_create_author(client):
    author_data = {"name": "lermontov"}
    response = await client.post("/authors/", json=author_data)
    assert response.status_code == 201


async def test_get_author(client):
    author_data = {"name": "svetaeva"}
    response = await client.post("/authors/", json=author_data)
    author_id = response.json()["id"]
    response = await client.get(f"/authors/{author_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "svetaeva"


async def test_delete_author(client):
    response = await client.post("/authors/", json={"name": "nepetrov"})
    assert response.status_code == 201
    author_id = response.json()["id"]
    response = await client.delete(f"/authors/{author_id}")
    assert response.status_code == 204
    assert not response.content


async def test_create_book(client):
    author_data = {"name": "gogol"}
    author_response = await client.post("/authors/", json=author_data)
    author_id = author_response.json()["id"]
    book_data = {"title": "dead souls"}
    response = await client.post(f"/books/{author_id}", json=book_data)
    assert response.status_code == 200
    assert response.json()["title"] == "dead souls"


async def test_get_books(client):
    response = await client.get("/books/")
    assert response.status_code == 200
    books = response.json()
    assert isinstance(books, list)


async def test_get_book(client):
    author_data = {"name": "tolstoi"}
    author_response = await client.post("/authors/", json=author_data)
    author_id = author_response.json()["id"]
    book_data = {"title": "war and peace"}
    book_response = await client.post(f"/books/{author_id}", json=book_data)
    book_id = book_response.json()["id"]
    response = await client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "war and peace"


async def test_delete_book(client):
    author_data = {"name": "tolstoi"}
    author_response = await client.post("/authors/", json=author_data)
    author_id = author_response.json()["id"]
    book_data = {"title": "karenina"}
    book_response = await client.post(f"/books/{author_id}", json=book_data)
    book_id = book_response.json()["id"]
    delete_response = await client.delete(f"/books/{book_id}")
    assert delete_response.status_code == 200
    get_response = await client.get(f"/books/{book_id}")
    assert get_response.status_code == 404