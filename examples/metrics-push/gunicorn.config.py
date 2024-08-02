from uuid import uuid4

from gunicorn.workers.sync import SyncWorker
from opentelemetry.sdk.resources import Resource, ResourceAttributes
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

# Either one of the following exporters can be used
# from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter

from utils import env, otel


bind = "0.0.0.0:{}".format(env.PORT)
workers = 2
threads = 10
timeout = 60
worker_class = "sync"


def post_fork(server, worker: SyncWorker) -> None:
    server.log.info("Worker spawned (pid: %s)", worker.pid)

    # Resource for adding common metadata to all signals (logs, metrics, traces)
    resource = Resource.create(
        attributes={
            ResourceAttributes.SERVICE_NAME: "example",
            ResourceAttributes.SERVICE_INSTANCE_ID: str(uuid4()),
            ResourceAttributes.PROCESS_PID: worker.pid,
        }
    )

    # Use opentelemetry.metrics and push metrics to OTLP Collector
    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=env.OTEL_EXPORTER_OTLP_ENDPOINT),
        export_interval_millis=env.OTEL_METRIC_EXPORT_INTERVAL,
    )

    otel.init_metrics(resource, metric_reader)

    otel.init_logging(resource)
