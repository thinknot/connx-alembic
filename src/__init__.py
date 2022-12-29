from json import encoder
from logging.config import dictConfig

import connexion
from flask import Flask, current_app
from werkzeug.exceptions import BadRequest, HTTPException

from .blueprint import core_views
from .flapp.config import app_settings, openapi_dir, template_dir
from .flapp.extension import db, ma

dictConfig(
    {
        "version": 1,
        "handlers": {"syslog": {"class": "logging.handlers.SysLogHandler"}},
        "root": {"handlers": ["syslog"]},
    }
)


def init_flask_app(devmode=False):
    connex_app = connexion.FlaskApp(
        __name__,
        specification_dir=openapi_dir,
        # options={"swagger_ui": False, "serve_spec": False},
    )
    # user framework application root path
    root_dir = connex_app.get_root_path()
    # flask app inside of connexion app
    app = connex_app.app

    app.logger.info("Loading APP_SETTINGS configuration from flapp/config.py")
    app.config.from_object(app_settings)
    app.static_url_path = "/static"
    app.template_folder = template_dir
    app.debug = devmode

    app.logger.debug("Initializing sqlalchemy")
    db.init_app(app)
    app.logger.debug("Initializing marshmallow")
    ma.init_app(app)

    app.logger.debug("Loading flask blueprints")
    with app.app_context():
        init_register_blueprints()

    app.logger.debug("Initializing OpenAPI connexion")
    connex_app.add_api("swagger.yml")

    app.json_encoder = encoder.JSONEncoder
    return app


def init_register_blueprints():
    current_app.register_blueprint(core_views.blueprint)
