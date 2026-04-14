# h2pcontrol Server Template

This project serves as a template for implementing h2pcontrol servers.

## Requirements

- Python 3.14+
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
heartbeat_interval_s = 5

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

## Format and linting

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting.

Check for lint issues:

```bash
uv run ruff check src/
```

Check for type issues:

```bash
 uv run pyright src/          
```

Format code:

```bash
uv run ruff format src/
```

These checks also run automatically on every pull request and pushes to main via
the [GitHub Actions workflow](.github/workflows/lint.yml)

## Proto dependencies

Generated code is pulled from the [Buf Schema Registry](https://buf.build/beyer-labs/h2pcontrol) via the
`buf.build/gen/python` index configured in `pyproject.toml`. To update to the latest proto versions:

```bash
uv sync --upgrade
```