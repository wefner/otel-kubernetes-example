#!/usr/bin/env python

from otel_tracing import setup_tracing
from otel_logging import setup_logging

import requests
import os

from requests.exceptions import HTTPError
from flask import Flask, jsonify, abort
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

app = Flask(__name__)
logger = setup_logging()

FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()


@app.route('/favicon.ico')
def favicon():
    return {}


@app.errorhandler(500)
def internal_error(error):
    return "500 error"


@app.route("/<endpoint>")
def get_activities(endpoint):
    url = f"{os.environ.get('BACKEND_SERVER_ENDPOINT')}/{endpoint}"

    response = None
    current_span = trace.get_current_span()

    try:
        if endpoint == "foo":
            raise HTTPError

        logger.warning("Getting an activity")
        logger.info("Getting activity!!")
        response = requests.get(url)

        if response.status_code == 200:
            logger.warning("Request okay")

    except HTTPError as http_error:
        msg = f"Couldn't get internal endpoint {os.environ.get('BACKEND_SERVER_ENDPOINT')}/{endpoint}"
        logger.error(msg)
        current_span.set_status(Status(StatusCode.ERROR))
        current_span.record_exception(http_error, attributes={"exception.message": msg})
        abort(500)

    return jsonify({"status": response.status_code, "activity": response.json()})


def main():
    setup_tracing()
    app.run(host=os.environ.get("POD_IP"), port=5000)


if __name__ == "__main__":
    main()
