import logging
from json import encoder

import connexion
from flask import Flask, current_app
from werkzeug.exceptions import BadRequest, HTTPException

from .blueprint import core_views
from .flapp.config import app_settings, openapi_path, template_dir
from .flapp.extension import db, ma


def init_flask_app(devmode=False):
    logging.debug("Creating a FlaskConnexion...")
    connex_app = connexion.FlaskApp(
        __name__,
        specification_dir=openapi_path,
        # options={"swagger_ui": False, "serve_spec": False},
    )
    # user framework application root path
    root_dir = connex_app.get_root_path()

    app = connex_app.app

    logging.info("Loading APP_SETTINGS configuration from flapp/config.py")
    app.config.from_object(app_settings)
    app.static_url_path = "/static"
    app.template_folder = template_dir
    app.debug = devmode

    logging.debug("Initializing sqlalchemy")
    db.init_app(app)
    logging.debug("Initializing marshmallow")
    ma.init_app(app)

    with app.app_context():
        logging.debug("Loading flask blueprints)")
        init_register_blueprints()

    connex_app.add_api("swagger.yml")
    app.json_encoder = encoder.JSONEncoder
    return app


def init_register_blueprints():
    current_app.register_blueprint(core_views.blueprint)
