import os
from opentelemetry import metrics
from flask import Flask
from prometheus_client import start_http_server, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from utils import env

app = Flask(__name__)

# Only one of the following configurations should be enabled at a time
#   - Start Prometheus client to expose metrics to expose metrics on a separate port
start_http_server(env.METRICS_PORT)
#   - Add prometheus wsgi middleware to expose metrics on /metrics
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})

meter = metrics.get_meter("example")
# Create example counters (will be kept in memory)
num_requests = meter.create_counter("num_requests", description="Number of requests")
error_count = meter.create_counter("error_count", description="Number of errors")


@app.route("/")
def hello():
    num_requests.add(1)

    # Raise an error randomly
    try:
        if os.urandom(1) > b"0":
            raise ValueError()
    except ValueError as e:
        # Increment the error count
        error_count.add(1)

    return "Hello from {}!".format(os.getpid())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.PORT)
