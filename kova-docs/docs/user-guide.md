# User Guide

In order to use Kova, you will need several services running.

## Supporting services

- a NATS server (required by all `kova` services)
- a database server (required for user authentication)

!!! note
    Running both services on the same machine is fine for development

## Installation

### Install `nsc`

```bash
$ brew tap nats-io/nats-tools
$ brew install nats-io/nats-tools/nsc

# to uninstall:
$ brew uninstall nats-io/nats-tools/nsc
$ brew untap nats-io/nats-tools
```

### Configuration

!!! warning
    After creating a NATS Operator, set it up by adding your `operator.jwt` on your NATS server in the `server.conf` file.
