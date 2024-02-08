#!/usr/bin/env python

import logging
import os

from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

"""
Experimental API 

https://opentelemetry-python.readthedocs.io/en/latest/examples/logs/README.html

There is a bug where INFO levels are not logged.

https://github.com/open-telemetry/opentelemetry-python/issues/3473

"""


def setup_logging():
    logger_provider = LoggerProvider()
    set_logger_provider(logger_provider)

    otlp_log_exporter = OTLPLogExporter(
        endpoint=os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT"), insecure=True
    )
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(otlp_log_exporter))
    handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
    logging.getLogger().addHandler(handler)

    logger = logging.getLogger(__name__)
    return logger
