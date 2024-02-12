#!/usr/bin/env python

import os
import requests
from datetime import datetime

from otel_tracing import setup_tracing
from otel_logging import setup_logging
from pymongo import MongoClient
from flask import Flask, jsonify
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.trace import SpanAttributes
from otel_metrics import ACTIVITIES_API_DURATION_HISTOGRAM


tracer = trace.get_tracer(__name__)
logger = setup_logging()

app = Flask(__name__)

client = MongoClient(os.environ.get("MONGODB_CONNECTION_STRING"))

FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()


@app.route("/activities")
def get_activities():
    start_time = datetime.now()

    url = "https://www.boredapi.com/api/activity"
    response = requests.get(url)

    duration_milliseconds = round((datetime.now() - start_time).total_seconds() * 1000)

    ACTIVITIES_API_DURATION_HISTOGRAM.record(
        duration_milliseconds, {"status_code": response.status_code}
    )

    with tracer.start_as_current_span("MongoDB Connection"):
        otel_db = client.otel
        activities_collection = otel_db.activities

        with tracer.start_as_current_span("activities.insertOne"):
            current_span = trace.get_current_span()
            current_span.add_event("Inserting activity into collection.")
            current_span.set_attribute(
                SpanAttributes.DB_MONGODB_COLLECTION, "activities"
            )
            current_span.set_attribute(SpanAttributes.DB_NAME, "otel")
            current_span.set_attribute(SpanAttributes.DB_OPERATION, "insertOne")

            activity = activities_collection.insert_one(response.json()).inserted_id
            logger.warning(f"Logged with id {activity}")

    return response.json()


def main():
    # https://opentelemetry.io/docs/specs/semconv/database/mongodb/
    mongodb_resource = Resource.create(
        attributes={
            "db.system": "mongodb",
            "db.user": "admin",
            "server.port": client.PORT,
            "server.address": client.HOST,
        }
    )
    setup_tracing(resource=mongodb_resource)

    app.run(host=os.environ.get("POD_IP"), port=5000)


if __name__ == "__main__":
    main()
