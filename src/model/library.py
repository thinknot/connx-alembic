from ..flapp.extension import db
from datetime import datetime

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("person.id"))

    title = db.Column(db.String)


class Quote(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("person.id"))
    author = db.relationship(
        "Person", 
        backref=db.backref("quotes", lazy="dynamic")
    )

    quote_text = db.Column(db.String, nullable=False)
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)
