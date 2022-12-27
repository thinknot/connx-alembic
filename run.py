import logging
import sys
import traceback

from werkzeug.exceptions import HTTPException
from werkzeug.serving import WSGIRequestHandler, _log

from src import init_flask_app

print(sys.path)


class MyRequestHandler(WSGIRequestHandler):
    # Just like WSGIRequestHandler, but without "- - [date]"
    def log(self, type, message, *args):
        _log(type, "%s %s\n" % (self.address_string(), message % args))


is_main = __name__ == "__main__"
console_flaskapp = init_flask_app(devmode=is_main)


def main():
    logging.warning("Flask MAIN")
    logging.info("Running main() in flask-debug mode. Security Risk!")
    logging.debug(console_flaskapp.static_url_path)
    logging.debug(console_flaskapp.static_folder)

    with console_flaskapp.app_context():
        from src.build_workdb import rebuild_db
        rebuild_db()

    console_flaskapp.run(debug=True, port=8008, request_handler=MyRequestHandler)


def wsgi():
    logging.debug("Flask WSGI")
    logging.info("Loading wsgi() in production mode.")
    gunicorn_logger = logging.getLogger("gunicorn.error")
    console_flaskapp.handlers = gunicorn_logger.handlers

    logging.info(
        f"Setting flask log level {gunicorn_logger.level} to match gunicorn log level"
    )
    console_flaskapp.logger.setLevel(gunicorn_logger.level)


@console_flaskapp.errorhandler(Exception)
def exception_handler(error):
    # pass through HTTP errors
    if isinstance(error, HTTPException):
        return error

    # now you're handling non-HTTP exceptions only
    logging.critical(repr(error))
    logging.error(error)
    logging.warning(traceback.format_exc())

    raise


if is_main:
    main()
else:
    wsgi()
