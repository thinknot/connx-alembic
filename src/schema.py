from flask_marshmallow import Marshmallow

from config import db, ma
from model import Person


class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        load_instance = True
        sqla_session = db.session


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


person_schema = PersonSchema()
people_schema = PersonSchema(many=True)
