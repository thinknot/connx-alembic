from marshmallow import fields, pre_load

from .flapp.extension import db, ma
from .model.ublog import Note, Person
from .model.library import Book, Quote

# Custom validator
def must_not_be_blank(data):
    if not data:
        raise ValidationError("Data not provided.")


class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Note
        load_instance = True
        sqla_session = db.session
        include_fk = True


class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    # https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html#marshmallow.fields.Nested
    notes = fields.Nested(NoteSchema, many=True)
    books = ma.auto_field()

    formatted_name = fields.Method("format_name", dump_only=True)

    def format_name(self, person):
        return f"{person.lname}, {person.fname}"


class ShipmentSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "item",
            "description",
            "status",
            "tracking_number",
            "current_location",
            "source",
            "destination",
            "description",
            "arrival",
        )



class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        include_fk = True

class QuoteSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    author = fields.Nested(PersonSchema, validate=must_not_be_blank)
    quote_text = fields.Str(required=True, validate=must_not_be_blank)
    posted_at = fields.DateTime(dump_only=True)

    # Allow client to pass author's full name in request body
    # e.g. {"author': 'Tim Peters"} rather than {"first": "Tim", "last": "Peters"}
    @pre_load
    def process_author(self, data, **kwargs):
        author_name = data.get("author")
        if author_name:
            first, last = author_name.split(" ")
            author_dict = dict(fname=first, lname=last)
        else:
            author_dict = {}
        data["author"] = author_dict
        return data
