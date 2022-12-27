from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from .flapp.extension import db


class Note(db.Model):
    __tablename__ = "note"
    id = db.Column(db.Integer, primary_key=True)
    # relate Note.person_id to Person using Person.id as primary key.
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"))
    # actual text payload of the note
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(
        # creation or update time
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


class Person(db.Model):
    __tablename__ = "person"
    id = db.Column(db.Integer, primary_key=True)
    # using lname as the identifier for a person in api calls
    lname = db.Column(db.String(32), unique=True)
    fname = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    #  relationship to the Person class
    notes = db.relationship(
        # you could use "Note" instead of Note here.
        Note,
        # Each instance of Note will contain an attribute called .person
        backref="person",
        # how to treat Note instances when changes are made to the parent Person
        # https://docs.sqlalchemy.org/en/latest/orm/cascades.html#delete
        cascade="all, delete, delete-orphan",
        # required if delete-orphan cascade. each Note has only a single parent
        single_parent=True,
        # sort the notes in descending order from newest to oldest
        order_by="desc(Note.timestamp)",
    )


class Shipment(db.Model):
    """
    Shipment Model
    """

    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(80))
    source = db.Column(db.String(120))
    current_location = db.Column(db.String(120))
    status = db.Column(db.String(120))
    item = db.Column(db.String(120))
    description = db.Column(db.String(120))
    tracking_number = db.Column(db.String(120), nullable=True)
    arrival = db.Column(db.String(120))

    def __repr__(self):
        return "<Shipment %r>" % self.item

    def __init__(
        self,
        description,
        source,
        current_location,
        status,
        item,
        tracking_number,
        arrival,
        destination,
    ):

        self.description = description
        self.destination = destination
        self.source = source
        self.current_location = current_location
        self.status = status
        self.item = item
        self.tracking_number = tracking_number
        self.arrival = arrival
