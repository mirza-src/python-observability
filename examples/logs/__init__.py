import os
import logging
from random import randint
from opentelemetry.semconv.trace import SpanAttributes
from flask import Flask
from utils import env

app = Flask(__name__)


@app.route("/")
def hello():
    logging.info("Request received")
    # Raise an error randomly
    try:
        if randint(0, 1):
            raise ValueError()
    except ValueError as err:
        logging.error(
            "A random error occurred",
            exc_info=err,
            extra={SpanAttributes.HTTP_METHOD: "GET", SpanAttributes.HTTP_ROUTE: "/"},
        )

    return "Hello from {}!".format(os.getpid())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.PORT)
