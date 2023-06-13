# Messages

## NATS messages

NATS messages are composed of several fields :

- A subject : The queue on which the message is published
- A payload : A byte array that is the message body
- A reply address (Optional) : The address the client or server can reply


## Protobuf messages

We use protobuf messages to allow for more flexibility and structure in the body of the message. The protobuf messages are indeed converted in bytes array and used as the payload of the NATS messages.
Three protobuf message types are used in our examples : `PingRequest`, `EchoRequest`, `EchoReply`.
These message types are defined in the `proto`and `kova/protocols` files.

### New message type

To create your own message type, write a `proto` file such as `proto/ping.proto`.
````python
syntax = "proto3";

package echo;

message EchoRequest {
  string message = 1;
}
````

Then create the protobuf messages thanks to the command line :
````commandline
poetry run protoc --proto_path=proto --python_out=kova/protocol proto/ping.proto
````

This will produce the `kova/protocol/ping_pb2.py` file needed to use the message later.

It is then needed to create the `kova/protocol/ping_pb2.pyi` file which is the actual class descriptor of our message type.

````python
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class EchoRequest(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
````
