import logging

from flask import Blueprint, current_app, jsonify

blueprint = Blueprint("core", __name__)


# Health check endpoint - responds if service is healthy
@blueprint.route("/ok")
def check_ok():
    return "Web server is up and running!"


@blueprint.route("/log")
def check_log():
    logging.debug("root logger debug message")
    current_app.logger.debug("current_app debug message")
    logging.info("root logger info message")
    current_app.logger.info("current_app info log")
    current_app.logger.warning("current_app warn message")
    current_app.logger.error("current_app error message")
    current_app.logger.critical("current_app doom message")
    logging.critical("root logger doom log")

    return jsonify("hello whirled peas")


@blueprint.route("/rand/<int:num>")
def get_rand_number(num: int):
    rndo = randint(0, num) if num >= 0 else randint(num, 0)
    return f"A rando between 0 and {num}:  {rndo}"
