# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ping.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\nping.proto\x12\x04\x65\x63ho"\x1e\n\x0b\x45\x63hoRequest\x12\x0f\n\x07message\x18\x01 \x01(\t"\x1f\n\x0c\x45\x63hoResponse\x12\x0f\n\x07message\x18\x01 \x01(\tb\x06proto3'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "ping_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _ECHOREQUEST._serialized_start = 20
    _ECHOREQUEST._serialized_end = 50
    _ECHORESPONSE._serialized_start = 52
    _ECHORESPONSE._serialized_end = 83
# @@protoc_insertion_point(module_scope)
