# Flask + Gunicorn Observability Examples

This repository contains simple examples that show how you can add observability to Flask web applications that are deployed using multiple or single Gunicorn workers.

### Logging

With [Opentelemetry Python SDK](https://opentelemetry.io/docs/languages/python/instrumentation) a handler is created for the built-in `logging` module. All logs are transformed to conform to the [Opentelemetry Logs Data Model](https://opentelemetry.io/docs/specs/otel/logs/data-model/#log-and-event-record-definition). No additional changes/configuration should be required, although it might be required to fix current logging calls to pass the required parameters correctly.

### Metrics

For exposing metrics there are different examples depending on the _strategy_ (push or pull) and single or multiple `gunicorn` processes.

- **Pull Strategy**: The application will expose the metrics on endpoint that can be part of the same `Flask` application or a server listening on a different port. [Prometheus SDK](https://prometheus.github.io/client_python) will be used to create endpoints that expose metrics in prometheus _text-based_ representation. An external Prometheus server will be responsible for scraping metrics from these endpoints periodically. This method varies depending on the number of worker processes:

  - **Single Process**: [Opentelemetry Python SDK](https://opentelemetry.io/docs/languages/python/instrumentation) can be used to create and update metrics. The [Opentelemetry Prometheus Exporter](https://opentelemetry.io/docs/languages/python/exporters/#prometheus) can then be used to expose the metrics through a Prometheus metrics endpoint.

  - **Multi Process**: In multi processes, each worker process will have its own copy of the metrics and `gunicorn` will distribute incoming requests to different workers, leading to inconsistent metrics being scraped. Opentelemetry's prometheus exporter does not support this scenario but the _Prometheus SDK_ does. Prometheus supports [multiprocess mode](https://prometheus.github.io/client_python/multiprocess) (with some limitations) by utilising a common `PROMETHEUS_MULTIPROC_DIR` directory across the workers for keeping the metrics.

- **Push Strategy**: The application is responsible for exporting metrics periodically to an external running [OTLP Collector](https://github.com/open-telemetry/opentelemetry-collector). This can be achieved by using the [Opentelemetry OTLP Exporter](https://opentelemetry.io/docs/languages/python/exporters/#otlp). _Prometheus_ SDK will not be required in this case and the application will also be responsible for determining the sampling rate (the export interval) available for the metrics. As each `gunicorn` worker can push their own metrics independently which can then be aggregated (or not), the number of worker processes do not need any consideration.

### Traces

TODO

## Setup

### Prerequisites

The repository includes a [Nix Flake](https://nix.dev/concepts/flakes.html) for easy setup. Be sure to [enable flakes](https://nixos.wiki/wiki/Flakes) in your Nix installation.

If you do not have Nix installed, run the following command for the complete setup using the [Determinate Nix Installer](https://github.com/DeterminateSystems/nix-installer):

```bash
curl  --proto  '=https'  --tlsv1.2  -sSf  -L  https://install.determinate.systems/nix | sh  -s  --  install
```

### Getting Started

- Clone this repository and run the following command to enter the configured Nix development shell:

```bash
nix develop
```

- Run one of the examples using the example task, e.g. `task example -- metrics-push`

### Examples

All the available examples can be found under the `examples` directory. Pass the example name to the `task example` command to run an example, e.g. `task example -- metrics-push`.

#### Available Examples

- metrics-push
- metrics-single-process-pull
- metrics-multi-process-pull
- logs
