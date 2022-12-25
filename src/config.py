import pathlib

import connexion
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

basedir = pathlib.Path(__file__).parent.resolve()
template_dir = basedir.parent.joinpath("templates").resolve()

connex_app = connexion.App(__name__, specification_dir=basedir)

connex_app.add_api("swagger.yml")

app = connex_app.app
app.template_folder = template_dir

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'mishmash.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

ma = Marshmallow(app)
