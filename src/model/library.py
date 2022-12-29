from ..flapp.extension import db


class Author(db.Model):
    author_id = db.Column(db.Integer, primary_key=True)
    books = db.relationship("Book", backref="author")

    name = db.Column(db.String)

    def __repr__(self):
        return f"<Author: {self.books}>"


class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("author.author_id"))

    title = db.Column(db.String)