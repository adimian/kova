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

To configurate the Authentication in the `kova` service, use the `nsc` service at the `/new-setup` endpoint

!!! warning
    After creating a NATS Operator, set it up by adding your `operator.jwt` on your NATS server in the `server.conf` file.

## Running the applicative server

!!! important
    There must be a NATS server properly configured and running. If needed, the NATS server access can be changed trough `Settings`

```bash
$ python server.py [--creds <credential_file.creds>]
```

## Running a client

!!! important
    There must be an applicative server listening to the same queue in order to process the mesages send by the clients

```bash
$ python client.py -s <nats-server> [--creds <credential_file.creds>]
```

nats-server is the IP address of your NATS server such as `nats://localhost:4222`

## Running the `nsc` service

```bash
$ python kova/authentication/nsc_api.py
```
