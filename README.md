# kova

🔨Message-based framework for buildling resilient mobile backends

## Description

## Installation

## Usage

## Support

## Roadmap

## Contributing

1. clone this repository
2. `make develop` to install all dependencies
3. `docker-compose up -d` to run external services locally

### Echo server
In terminal A (server) : `python kova/server.py --creds <path to credential file (.creds)> --queue <queue to use, by default echo>`

In terminal B (client) : `python scripts/nats-pub.py -s <server ip> -- creds <path to credential file (.creds) [--request] test.echo`

## Authors and acknowledgment
Kova is brought to you by the following contributors:
- Adimian Studio

## License
Apache License, Version 2.0
