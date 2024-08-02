import os
from random import randint
from opentelemetry.semconv.trace import SpanAttributes
from flask import Flask, Response
from prometheus_client import (
    multiprocess,
    generate_latest,
    CollectorRegistry,
    CONTENT_TYPE_LATEST,
    Counter,
)

from utils import env

# Ensure the environment variables are set
assert env.PROMETHEUS_MULTIPROC_DIR, "PROMETHEUS_MULTIPROC_DIR must be set"

app = Flask(__name__)

# Create example counters (will be kept in memory) directly using prometheus_client
num_requests = Counter("num_requests", "Number of requests")
error_count = Counter("error_count", "Number of errors")


@app.route("/")
def hello():
    # Increment the number of requests
    num_requests.inc()

    # Raise an error randomly
    try:
        if randint(0, 1):
            raise ValueError()
    except:
        # Increment the error count
        error_count.inc()

    return "Hello from {}!".format(os.getpid())


@app.route("/metrics")
def metrics():
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    data = generate_latest(registry)
    return Response(data, mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.PORT)
