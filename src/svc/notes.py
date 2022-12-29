from flask import Response, abort, make_response

from ..flapp.extension import db
from ..model.ublog import Note, Person
from ..schema import NoteSchema

note_schema = NoteSchema()


def read_one(note_id: int) -> dict:
    note = Note.query.get(note_id)

    if note is None:
        abort(404, f"Note with ID {note_id} not found")
    else:
        return note_schema.dump(note)


def update(note_id: int, note) -> tuple[dict, int]:
    existing_note = Note.query.get(note_id)

    if existing_note:
        update_note = note_schema.load(note, session=db.session)
        existing_note.content = update_note.content
        db.session.merge(existing_note)
        db.session.commit()
        return note_schema.dump(existing_note), 201
    else:
        abort(404, f"Note with ID {note_id} not found")


def delete(note_id: int) -> Response:
    existing_note = Note.query.get(note_id)

    if existing_note:
        db.session.delete(existing_note)
        db.session.commit()
        return make_response(f"{note_id} successfully deleted", 204)
    else:
        abort(404, f"Note with ID {note_id} not found")


def create(note: Note) -> tuple[dict, int]:
    # A note always needs a person owner
    person_id = note.get("person_id")
    person = Person.query.get(person_id)

    if person:
        # append the new note to person.notes
        new_note = note_schema.load(note, session=db.session)
        person.notes.append(new_note)
        # SQLAlchemy will add to the note table.
        db.session.commit()
        return note_schema.dump(new_note), 201
    else:
        abort(404, f"Person not found for ID: {person_id}")
