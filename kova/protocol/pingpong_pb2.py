# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pingpong.proto

import sys

_b = (
    sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))
)
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="pingpong.proto",
    package="pingpong",
    syntax="proto3",
    serialized_pb=_b(
        '\n\x0epingpong.proto\x12\x08pingpong"C\n\x0bPingRequest\x12\x13\n\x0b\x64\x65stination\x18\x01 \x01(\t\x12\x0e\n\x06origin\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\tb\x06proto3'
    ),
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


_PINGREQUEST = _descriptor.Descriptor(
    name="PingRequest",
    full_name="pingpong.PingRequest",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="destination",
            full_name="pingpong.PingRequest.destination",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name="origin",
            full_name="pingpong.PingRequest.origin",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
        _descriptor.FieldDescriptor(
            name="message",
            full_name="pingpong.PingRequest.message",
            index=2,
            number=3,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=28,
    serialized_end=95,
)

DESCRIPTOR.message_types_by_name["PingRequest"] = _PINGREQUEST

PingRequest = _reflection.GeneratedProtocolMessageType(
    "PingRequest",
    (_message.Message,),
    dict(
        DESCRIPTOR=_PINGREQUEST,
        __module__="pingpong_pb2"
        # @@protoc_insertion_point(class_scope:pingpong.PingRequest)
    ),
)
_sym_db.RegisterMessage(PingRequest)


# @@protoc_insertion_point(module_scope)
