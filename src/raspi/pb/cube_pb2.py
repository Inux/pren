# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cube.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='cube.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\ncube.proto\"\x15\n\x04\x43ube\x12\r\n\x05state\x18\x01 \x01(\x05\x62\x06proto3')
)




_CUBE = _descriptor.Descriptor(
  name='Cube',
  full_name='Cube',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='state', full_name='Cube.state', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=14,
  serialized_end=35,
)

DESCRIPTOR.message_types_by_name['Cube'] = _CUBE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Cube = _reflection.GeneratedProtocolMessageType('Cube', (_message.Message,), dict(
  DESCRIPTOR = _CUBE,
  __module__ = 'cube_pb2'
  # @@protoc_insertion_point(class_scope:Cube)
  ))
_sym_db.RegisterMessage(Cube)


# @@protoc_insertion_point(module_scope)
