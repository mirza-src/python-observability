from uuid import uuid4

from gunicorn.workers.sync import SyncWorker
from opentelemetry.sdk.resources import Resource, ResourceAttributes
from opentelemetry.exporter.prometheus import PrometheusMetricReader

from utils import env, otel


bind = "0.0.0.0:{}".format(env.PORT)
workers = 1
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

    # Use opentelemetry.metrics but export using prometheus_client in each worker
    metric_reader = PrometheusMetricReader()
    otel.init_metrics(resource, metric_reader)

    otel.init_logging(resource)
