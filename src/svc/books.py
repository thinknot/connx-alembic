from flask import Response, abort, make_response

from ..flapp.extension import db
from ..model.ublog import Person
from ..model.library import Book
from ..schema import BookSchema

book_schema = BookSchema()


def read_one(book_id: int) -> dict:
    book = Book.query.get(book_id)

    if book is None:
        abort(404, f"Book with ID {book_id} not found")
    else:
        return book_schema.dump(book)


def update(book_id: int, book) -> tuple[dict, int]:
    existing_book = Book.query.get(book_id)

    if existing_book:
        update_book = book_schema.load(book, session=db.session)
        existing_book.title = update_book.title
        db.session.merge(existing_book)
        db.session.commit()
        return book_schema.dump(existing_book), 201
    else:
        abort(404, f"Book with ID {book_id} not found")


def delete(book_id: int) -> Response:
    existing_book = Book.query.get(book_id)

    if existing_book:
        db.session.delete(existing_book)
        db.session.commit()
        return make_response(f"{book_id} successfully deleted", 204)
    else:
        abort(404, f"Book with ID {book_id} not found")


def create(book: Book) -> tuple[dict, int]:
    # A book always needs a person author/owner
    person_id = book.get("person_id")
    person = Person.query.get(person_id)

    if person:
        # append the new book to person.books
        new_book = book_schema.load(book, session=db.session)
        person.books.append(new_book)
        # SQLAlchemy will add to the book table.
        db.session.commit()
        return book_schema.dump(new_book), 201
    else:
        abort(404, f"Person not found for ID: {person_id}")
