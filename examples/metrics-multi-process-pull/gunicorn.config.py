from uuid import uuid4

from gunicorn.workers.sync import SyncWorker
from opentelemetry.sdk.resources import Resource, ResourceAttributes

from utils import env, otel


bind = "0.0.0.0:{}".format(env.PORT)
workers = 2
threads = 10
timeout = 60
worker_class = "sync"


def when_ready(server) -> None:
    server.log.info("Server is ready. Spawning workers")

    # Cannot use opentelemetry.metrics in a multi-process environment
    # Directly use prometheus_client in each worker
    # Clear prometheus metrics from previous runs
    otel.clear_prometheus_metrics()


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

    otel.init_logging(resource)
