# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: auth_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12\x61uth_service.proto\x12\x04\x61uth\"1\n\x0b\x41uthRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"0\n\x0c\x41uthResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"-\n\x0bQuizRequest\x12\r\n\x05token\x18\x01 \x01(\t\x12\x0f\n\x07\x61nswers\x18\x02 \x03(\x05\"K\n\x0cQuizResponse\x12\x11\n\tquestions\x18\x01 \x03(\t\x12\x0f\n\x07options\x18\x02 \x03(\t\x12\x17\n\x0f\x63orrect_answers\x18\x03 \x01(\x05\x32s\n\x0b\x41uthService\x12\x35\n\x0c\x41uthenticate\x12\x11.auth.AuthRequest\x1a\x12.auth.AuthResponse\x12-\n\x04Quiz\x12\x11.auth.QuizRequest\x1a\x12.auth.QuizResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'auth_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _AUTHREQUEST._serialized_start=28
  _AUTHREQUEST._serialized_end=77
  _AUTHRESPONSE._serialized_start=79
  _AUTHRESPONSE._serialized_end=127
  _QUIZREQUEST._serialized_start=129
  _QUIZREQUEST._serialized_end=174
  _QUIZRESPONSE._serialized_start=176
  _QUIZRESPONSE._serialized_end=251
  _AUTHSERVICE._serialized_start=253
  _AUTHSERVICE._serialized_end=368
# @@protoc_insertion_point(module_scope)
