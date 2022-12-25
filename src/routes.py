from random import randint

from flask import current_app, render_template

from model import Person


@current_app.route("/")
def home():
    people = Person.query.all()
    return render_template("hom.html", people=people)
