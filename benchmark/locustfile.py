import random
import time

import pynats
from locust import User, task, between

from kova.protocol.pingpong_pb2 import PingRequest


class OnRequest:
    def __init__(self, environment, request_type, identifier):
        self.environment = environment
        self.identifier = identifier
        self.request_type = request_type
        self.start = None
        self.response_length = 0

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def set_response(self, resp):
        self.response_length = len(resp)

    def __exit__(self, exc_type, exc_val, exc_tb):
        response_time = (time.perf_counter() - self.start) * 1000
        self.environment.events.request.fire(
            request_type=self.request_type,
            name=self.identifier,
            start_time=self.start,
            response_time=response_time,
            response_length=self.response_length,
            exception=exc_type,
        )


class MyUser(User):
    wait_time = between(1, 5)

    def __init__(self, environment):
        super().__init__(environment)
        self.environment = environment
        self.client: pynats.NATSClient | None = None

    def on_start(self):
        self.client = pynats.NATSClient(**self.params)
        self.client.connect()

    @property
    def params(self):
        return {
            "url": random.choice(
                [
                    "nats://localhost:4222",
                ]
            ),
            "socket_timeout": 5,
        }

    @task
    def task1(self):
        with OnRequest(
            environment=self.environment,
            identifier="pong",
            request_type="PONG",
        ):

            def ping_handler(msg):
                req = PingRequest.FromString(msg.data)
                if req.origin != "test2.ping":
                    res = PingRequest()
                    res.destination = req.origin
                    res.origin = "test2.ping"
                    res.message = "pong"
                    payload = res.SerializeToString()

                    self.client.publish("test2.ping", payload)

            try:
                self.client.subscribe("test2.ping", callback=ping_handler)
            except (OSError, TimeoutError, BrokenPipeError):
                self.client.connect()
                raise

    @task
    def task2(self):
        with OnRequest(
            environment=self.environment,
            identifier="ping",
            request_type="PING",
        ):

            req = PingRequest()
            req.destination = "test2"
            req.message = "ping"
            req.origin = "test.ping"
            payload = req.SerializeToString()

            def pong_handler(msg):
                req = PingRequest.FromString(msg.data)
                print(
                    f"Received a message on [{msg.subject}]: '{req.message}'"
                )

            try:
                self.client.publish(subject="test.ping", payload=payload)
                self.client.subscribe("test.ping", callback=pong_handler)
            except (OSError, TimeoutError, BrokenPipeError):
                self.client.connect()
                raise
