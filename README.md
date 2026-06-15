# h2pcontrol Server Template

This project serves as a both a template for implementing h2pcontrol servers,
and a concrete  implementation of the example service defined in the [h2pcontrol BSR.](https://buf.build/beyer-labs/h2pcontrol/docs/main%3Ah2pcontrol.example.v1)

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Setup

```bash
uv sync
```

## Configuration

The server configuration is stored in [config.toml](config.toml)

```toml
[manager]
address = "127.0.0.1:50051"
retry_interval_s = 5

[service]
name = "greeter"
description = "Greeter service"
host = "0.0.0.0"
port = 50055
```

These config values can be overridden using environment variables. For example, the manager address
could be overridden with a MANAGER__ADDRESS ENV var.

## Running

Use the following command to start the service:

```bash
uv run src/main.py
```

On start up, the service attempts to register with the h2pcontrol manager at the configured address.
If this fails (for example because the manager is not running),
a `WARN` log will be emitted.

## Usage

This example server implements a single "SayHello" endpoint.
It returns the provided text with "Hello," prepended.
If you have buf installed you can test the service by running the `buf curl`:

```shell
  buf curl --protocol grpc \
  --http2-prior-knowledge \
  --schema buf.build/beyer-labs/h2pcontrol \
  -d '{"name": "World"}' \
  "http://localhost:50055/h2pcontrol.example.v1.ExampleService/SayHello"  
```

## Adapting this template

Available services are defined in the [h2pcontrol Buf Schema Registry](https://buf.build/beyer-labs/h2pcontrol).

### 1. Replace the service implementation

Rename `src/service/example.py` to match your service (e.g. `src/service/greeter.py`) and replace its contents:

```python
from h2pcontrol.<package>.<name>_pb2 import ...
from h2pcontrol.<package>.<name>_pb2_grpc import <ServiceName>Servicer
from h2pcontrol.sdk import Server


class <ServiceName>(Server, <ServiceName>Servicer):
    # implement your server methods here
```

### 2. Update the re-export

In `src/service/__init__.py`, replace the import to match your new class:

```python
from .greeter import GreeterService as GreeterService
```

### 3. Update the entry point

In `src/main.py`, import your service class:

```python
from service import GreeterService
...
svc = GreeterService(cfg)
```

### 4. Update config and project name

In `config.toml`, set `name` and `description` under `[service]` to reflect your service.

In `pyproject.toml`, update the `name` field under `[project]`.

## Linting and formatting
This template comes with a [GitHub Actions Workflow](.github/workflows/lint.yml) that runs formatting and linting 
checks on each push to main and each pull request.
We reccomend using this as a status check prior to merging.

The workflow uses [Ruff](https://docs.astral.sh/ruff/) and [PyRight](https://github.com/microsoft/pyright).
You can run the same checks locally with the following commands:


Format code:

```bash
uv run ruff format src/
```

```bash
uv run ruff check src/
```

Check for type issues:

```bash
 uv run pyright src/          
```

## Proto dependencies

Generated code is pulled from the [Buf Schema Registry](https://buf.build/beyer-labs/h2pcontrol) via the
`buf.build/gen/python` index configured in `pyproject.toml`. To update to the latest proto versions:

```bash
uv sync --upgrade
```