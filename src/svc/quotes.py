from flask import Response, abort
from ..model.ublog import Person
from ..model.library import Quote
from ..schema import QuoteSchema
from ..flapp.extension import db

from sqlalchemy.exc import NoResultFound
from marshmallow import ValidationError

quote_schema = QuoteSchema()
quotes_schema = QuoteSchema(many=True, only=("id", "quote_text"))


def read_all():
    quotes = Quote.query.all()
    return quotes_schema.dump(quotes, many=True)

def read_one(pk):
    quote = Quote.query.filter(Quote.id == pk).one_or_none()
    if quote is None:
        abort(400, "Quote could not be found.")
    else:
        result = quote_schema.dump(quote)
        return {"quote": result}


def create(quote: Quote):
    # A note always needs a author owner
    person_id = quote.get("author_id")
    person = Person.query.get(person_id)

    if person is None:
        # Create a new author
        person = Person(fname=first, lname=last)
        # db.session.add(new_person)
    # Create new quote?
    new_quote = Quote(
        quote_text=quote.get("quote_text"),
        author=person
    )
    db.session.add(new_quote)
    db.session.commit()
    result = quote_schema.dump(new_quote), 201
    return {"message": "Created new quote.", "quote": result}
