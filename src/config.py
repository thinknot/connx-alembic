from pathlib import Path
from typing import Any, Dict

import connexion
import prance
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

basedir = Path(__file__).parent.resolve()
template_dir = basedir.parent.joinpath("templates").resolve()

connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app
app.template_folder = template_dir

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'mishmash.db'}"
# turns the SQLAlchemy event system off. The event system generates events
# that are useful in event-driven programs, but it adds significant overhead.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

ma = Marshmallow(app)
db = SQLAlchemy(app)
