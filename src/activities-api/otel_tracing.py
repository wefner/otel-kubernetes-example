#!/usr/bin/env python

import os

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry import trace


def setup_tracing(resource) -> None:
    otlp_exporter = OTLPSpanExporter(
        endpoint=os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT"), insecure=True
    )
    span_processor = BatchSpanProcessor(otlp_exporter)

    tp = TracerProvider(resource=resource)
    tp.add_span_processor(span_processor)
    trace.set_tracer_provider(tp)
