# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hearbeat.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='hearbeat.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0ehearbeat.proto\".\n\tHeartbeat\x12\x11\n\tcomponent\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\tb\x06proto3')
)




_HEARTBEAT = _descriptor.Descriptor(
  name='Heartbeat',
  full_name='Heartbeat',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='component', full_name='Heartbeat.component', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='Heartbeat.status', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=18,
  serialized_end=64,
)

DESCRIPTOR.message_types_by_name['Heartbeat'] = _HEARTBEAT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Heartbeat = _reflection.GeneratedProtocolMessageType('Heartbeat', (_message.Message,), dict(
  DESCRIPTOR = _HEARTBEAT,
  __module__ = 'hearbeat_pb2'
  # @@protoc_insertion_point(class_scope:Heartbeat)
  ))
_sym_db.RegisterMessage(Heartbeat)


# @@protoc_insertion_point(module_scope)
