from random import randint

from flask import render_template

import config
from model import Person

app = config.connex_app
app.add_api(config.basedir / "swagger.yml")


@app.route("/")
def home():
    people = Person.query.all()
    return render_template("hom.html", people=people)


@app.route("/rand/<int:num>")
def get_rand_number(num: int):
    rndo = randint(0, num) if num >= 0 else randint(num, 0)
    return f"A rando between 0 and {num}:  {rndo}"


if __name__ == "__main__":
    # db.init_app(app)
    app.run(host="0.0.0.0", port=8000, debug=True)
