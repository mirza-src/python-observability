import glob
import os
import logging
import json
from opentelemetry import _logs, metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import MetricReader
from opentelemetry.sdk._logs import LoggingHandler, LoggerProvider, LogRecord
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk._logs.export import (
    SimpleLogRecordProcessor,
    ConsoleLogExporter,
)
from utils import env


def clear_prometheus_metrics() -> None:
    os.makedirs(env.PROMETHEUS_MULTIPROC_DIR, exist_ok=True)
    for filepath in glob.glob(env.PROMETHEUS_MULTIPROC_DIR + "/*.db"):
        os.remove(filepath)


def init_metrics(resource: Resource, reader: MetricReader) -> None:
    metrics.set_meter_provider(
        MeterProvider(
            resource=resource,
            metric_readers=[reader],
        )
    )


def init_logging(resource: Resource) -> None:
    # HACK: The default Otel SDK completely ignores formatters when outputting the message being logged.
    # We overcome this by creating our own LoggingHandler class which respects formatters.
    class FormattedLoggingHandler(LoggingHandler):
        def emit(self, record: logging.LogRecord) -> None:
            msg = self.format(record)
            record.msg = msg
            record.args = None
            self._logger.emit(self._translate(record))

    def formatter_patch(r: LogRecord):
        # HACK: The default Otel SDK does not convert severity_number to number correctly.
        r.severity_number = r.severity_number.value
        # HACK: The default Otel SDK creates a formatted json string, we need a single line json string.
        result = json.dumps(json.loads(r.to_json())) + "\n"
        return result

    logger_provider = LoggerProvider(resource)
    logger_provider.add_log_record_processor(
        SimpleLogRecordProcessor(ConsoleLogExporter(formatter=formatter_patch))
    )
    _logs.set_logger_provider(logger_provider)
    handler = FormattedLoggingHandler(
        level=logging.NOTSET, logger_provider=logger_provider
    )
    # Add the handler to logging library
    logging.basicConfig(level=logging.NOTSET, handlers=[handler])
