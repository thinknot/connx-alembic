from random import randint

from flask import render_template

from config import app, connex_app
from model import db


@app.route("/")
def home():

    return render_template("hom.html")


@app.route("/rand/<int:num>")
def get_rand_number(num: int):
    rndo = randint(0, num) if num >= 0 else randint(num, 0)
    return f"A rando between 0 and {num}:  {rndo}"


if __name__ == "__main__":
    db.init_app(app)
    app.run(host="0.0.0.0", port=8000, debug=True)
