# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: speed.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='speed.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0bspeed.proto\"\x16\n\x05Speed\x12\r\n\x05speed\x18\x01 \x01(\x05\x62\x06proto3')
)




_SPEED = _descriptor.Descriptor(
  name='Speed',
  full_name='Speed',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='speed', full_name='Speed.speed', index=0,
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
  serialized_start=15,
  serialized_end=37,
)

DESCRIPTOR.message_types_by_name['Speed'] = _SPEED
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Speed = _reflection.GeneratedProtocolMessageType('Speed', (_message.Message,), dict(
  DESCRIPTOR = _SPEED,
  __module__ = 'speed_pb2'
  # @@protoc_insertion_point(class_scope:Speed)
  ))
_sym_db.RegisterMessage(Speed)


# @@protoc_insertion_point(module_scope)
