#!/usr/bin/env python

import os

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_NAME, SERVICE_VERSION, Resource
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter


def setup_metrics():
    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT"))
    )
    provider = MeterProvider(metric_readers=[metric_reader])

    # Sets the global default meter provider
    metrics.set_meter_provider(provider)

    # Creates a meter from the global meter provider
    meter = metrics.get_meter(__name__)
    return meter


meter = setup_metrics()

ACTIVITIES_API_DURATION_HISTOGRAM = meter.create_histogram(
    "activities_api_duration", unit="ms", description="Duration of request."
)
