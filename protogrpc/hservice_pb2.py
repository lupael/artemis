# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hservice.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='hservice.proto',
  package='hservice',
  syntax='proto3',
  serialized_pb=_b('\n\x0ehservice.proto\x12\x08hservice\"\x1c\n\x0eHformatMessage\x12\n\n\x02id\x18\x01 \x01(\x05\"\x07\n\x05\x45mpty2N\n\x0fMessageListener\x12;\n\x0cqueryHformat\x12\x18.hservice.HformatMessage\x1a\x0f.hservice.Empty\"\x00\x42\x32\n\x16\x61rtemis.io.grpc.protosB\rHServiceProtoP\x01\xa2\x02\x06HSRVCPb\x06proto3')
)




_HFORMATMESSAGE = _descriptor.Descriptor(
  name='HformatMessage',
  full_name='hservice.HformatMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='hservice.HformatMessage.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=28,
  serialized_end=56,
)


_EMPTY = _descriptor.Descriptor(
  name='Empty',
  full_name='hservice.Empty',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=58,
  serialized_end=65,
)

DESCRIPTOR.message_types_by_name['HformatMessage'] = _HFORMATMESSAGE
DESCRIPTOR.message_types_by_name['Empty'] = _EMPTY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

HformatMessage = _reflection.GeneratedProtocolMessageType('HformatMessage', (_message.Message,), dict(
  DESCRIPTOR = _HFORMATMESSAGE,
  __module__ = 'hservice_pb2'
  # @@protoc_insertion_point(class_scope:hservice.HformatMessage)
  ))
_sym_db.RegisterMessage(HformatMessage)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), dict(
  DESCRIPTOR = _EMPTY,
  __module__ = 'hservice_pb2'
  # @@protoc_insertion_point(class_scope:hservice.Empty)
  ))
_sym_db.RegisterMessage(Empty)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\026artemis.io.grpc.protosB\rHServiceProtoP\001\242\002\006HSRVCP'))

_MESSAGELISTENER = _descriptor.ServiceDescriptor(
  name='MessageListener',
  full_name='hservice.MessageListener',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=67,
  serialized_end=145,
  methods=[
  _descriptor.MethodDescriptor(
    name='queryHformat',
    full_name='hservice.MessageListener.queryHformat',
    index=0,
    containing_service=None,
    input_type=_HFORMATMESSAGE,
    output_type=_EMPTY,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_MESSAGELISTENER)

DESCRIPTOR.services_by_name['MessageListener'] = _MESSAGELISTENER

# @@protoc_insertion_point(module_scope)
