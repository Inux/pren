# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: current.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='current.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\rcurrent.proto\"\x1a\n\x07\x43urrent\x12\x0f\n\x07\x63urrent\x18\x01 \x01(\x05\x62\x06proto3')
)




_CURRENT = _descriptor.Descriptor(
  name='Current',
  full_name='Current',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='current', full_name='Current.current', index=0,
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
  serialized_start=17,
  serialized_end=43,
)

DESCRIPTOR.message_types_by_name['Current'] = _CURRENT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Current = _reflection.GeneratedProtocolMessageType('Current', (_message.Message,), dict(
  DESCRIPTOR = _CURRENT,
  __module__ = 'current_pb2'
  # @@protoc_insertion_point(class_scope:Current)
  ))
_sym_db.RegisterMessage(Current)


# @@protoc_insertion_point(module_scope)