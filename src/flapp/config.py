import configparser
import os
from pathlib import Path
from typing import Any, Dict

app_settings = os.getenv("APP_SETTINGS", "src.flapp.config.DevConfig")

app_dir = Path(__file__).parent.resolve()
base_dir = app_dir.parent.resolve()
template_dir = base_dir.parent.joinpath("templates").resolve()
abs_file_path = os.path.abspath(os.path.dirname(__file__))

if "SPEC_PATH" in os.environ:
    openapi_path = os.environ["SPEC_PATH"]
else:
    openapi_path = Path(abs_file_path).parent.resolve()


class Config:
    APP_DIR = base_dir

    FLASK_APP = "run:console_flaskapp"

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{base_dir / 'mishmash.db'}"

    # turns the SQLAlchemy event system off. The event system generates events
    # that are useful in event-driven programs, but it adds significant overhead.
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    FLASK_DEBUG = True
    TESTING = True
    DEBUG = True


class TestConfig(Config):
    FLASK_DEBUG = False
    TESTING = True
    DEBUG = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    WTF_CSRF_ENABLED = False
    # Our test emails/domain isn't necessarily valid
    SECURITY_EMAIL_VALIDATOR_ARGS = {"check_deliverability": False}
    # Make this plaintext for most tests - reduces unit test time by 50%
    SECURITY_PASSWORD_HASH = "plaintext"


class ProductionConfig(Config):
    FLASK_DEBUG = False
    TESTING = False
    DEBUG = False
