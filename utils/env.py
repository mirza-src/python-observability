import os
from opentelemetry.sdk.environment_variables import (
    OTEL_METRIC_EXPORT_INTERVAL,
    OTEL_EXPORTER_OTLP_ENDPOINT,
)

PORT = os.environ.get("PORT", 5100)
METRICS_PORT = os.environ.get("METRICS_PORT", 10250)
PROMETHEUS_MULTIPROC_DIR = os.environ.get("PROMETHEUS_MULTIPROC_DIR", "").rstrip("/")

# NOTE: Theses variables do not need to be accessed in the code, Otel SDK will automatically read them
OTEL_EXPORTER_OTLP_ENDPOINT = os.environ.get(OTEL_EXPORTER_OTLP_ENDPOINT)
# Should be > 15000 in production
OTEL_METRIC_EXPORT_INTERVAL = int(os.environ.get(OTEL_METRIC_EXPORT_INTERVAL, 3000))
