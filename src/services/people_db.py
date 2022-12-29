from flask import Response, abort, make_response

from ..flapp.extension import db
from ..model.ublog import Person
from ..schema import people_schema, person_schema


def read_all():
    # runs when server receives an HTTP request to GET /api/people
    people = Person.query.all()
    # works with what it receives and doesn’t filter out any data
    return people_schema.dump(people)


def read_one(lname: str) -> dict:
    person = Person.query.filter(Person.lname == lname).one_or_none()

    if person is not None:
        return person_schema.dump(person)
    else:
        abort(404, f"Person with last name {lname} not found")


def create(person) -> tuple[dict, int]:
    # request body must contain a last name

    lname = person.get("lname")
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()

    if existing_person is None:
        new_person = person_schema.load(person, session=db.session)
        db.session.add(new_person)
        db.session.commit()
        # respond with the new object and a 201 HTTP code
        return person_schema.dump(new_person), 201
    else:
        abort(406, f"Person with last name {lname} already exists")


def update(lname, person) -> tuple[dict, int]:
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()

    if existing_person:
        update_person = person_schema.load(person, session=db.session)
        existing_person.fname = update_person.fname
        db.session.merge(existing_person)
        db.session.commit()
        return person_schema.dump(existing_person), 201
    else:
        abort(404, f"Person with last name {lname} not found")


def delete(lname) -> Response:
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()

    if existing_person:
        db.session.delete(existing_person)
        db.session.commit()
        return make_response(f"{lname} successfully deleted", 200)
    else:
        abort(404, f"Person with last name {lname} not found")
