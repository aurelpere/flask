#!/usr/bin/python3
# coding: utf-8
"""
this is app.py for flask-tutorial (sondage example)
"""
from flask import Flask, request
# pylint: disable=import-error
from handlers.routes import configure_routes
from flask.logging import create_logger

# create the Flask app

app = Flask(__name__)
log = create_logger(app)
configure_routes(app)


@app.before_request
def log_request_info():
    log.debug('Headers: %s', request.headers)
    log.debug('Body: %s', request.get_data())


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, host="0.0.0.0", port=5000)
