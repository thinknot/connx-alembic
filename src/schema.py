from marshmallow_sqlalchemy import fields

from .flapp.extension import db, ma
from .model.ublog import Note, Person


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


note_schema = NoteSchema()
person_schema = PersonSchema()
people_schema = PersonSchema(many=True)
