import logging

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

logging.debug("Constructing flask extensions...")
ma = Marshmallow()
db = SQLAlchemy()
