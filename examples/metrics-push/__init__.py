import os
from random import randint
from opentelemetry import metrics
from opentelemetry.semconv.trace import SpanAttributes
from flask import Flask

from utils import env

app = Flask(__name__)

meter = metrics.get_meter("example")
# Create example counters (will be kept in memory)
num_requests = meter.create_counter("num_requests", description="Number of requests")
error_count = meter.create_counter("error_count", description="Number of errors")


@app.route("/")
def hello():
    # Increment the number of requests
    num_requests.add(1)

    # Raise an error randomly
    try:
        if randint(0, 1):
            raise ValueError()
    except:
        # Increment the error count
        error_count.add(1)

    return "Hello from {}!".format(os.getpid())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.PORT)
