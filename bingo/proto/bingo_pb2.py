# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/bingo.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11proto/bingo.proto\x12\x05\x62ingo\" \n\x0cLoginRequest\x12\x10\n\x08username\x18\x01 \x01(\t\"n\n\rLoginResponse\x12\r\n\x05token\x18\x01 \x01(\t\x12\x17\n\x0fplayersLoggedIn\x18\x02 \x03(\t\x12\x14\n\x0cplayersReady\x18\x03 \x03(\t\x12\x0e\n\x06status\x18\x04 \x01(\x05\x12\x0f\n\x07message\x18\x05 \x01(\t\"/\n\x0cReadyRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\r\n\x05token\x18\x02 \x01(\t\">\n\rReadyResponse\x12\x0c\n\x04\x63\x61rd\x18\x01 \x03(\x05\x12\x0e\n\x06status\x18\x02 \x01(\x05\x12\x0f\n\x07message\x18\x03 \x01(\t\".\n\x0bPlayRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\r\n\x05token\x18\x02 \x01(\t\"W\n\x12GameStatusResponse\x12\x0e\n\x06number\x18\x01 \x01(\x05\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x0e\n\x06status\x18\x03 \x01(\x05\x12\x0f\n\x07message\x18\x04 \x01(\t\"2\n\x0fWinCheckRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\r\n\x05token\x18\x02 \x01(\t\"3\n\x10WinCheckResponse\x12\x0e\n\x06status\x18\x01 \x01(\x05\x12\x0f\n\x07message\x18\x02 \x01(\t2\xe7\x01\n\x05\x42ingo\x12\x34\n\x05Login\x12\x13.bingo.LoginRequest\x1a\x14.bingo.LoginResponse0\x01\x12\x32\n\x05Ready\x12\x13.bingo.ReadyRequest\x1a\x14.bingo.ReadyResponse\x12\x37\n\x04Play\x12\x12.bingo.PlayRequest\x1a\x19.bingo.GameStatusResponse0\x01\x12;\n\x08\x43heckWin\x12\x16.bingo.WinCheckRequest\x1a\x17.bingo.WinCheckResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'proto.bingo_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _LOGINREQUEST._serialized_start=28
  _LOGINREQUEST._serialized_end=60
  _LOGINRESPONSE._serialized_start=62
  _LOGINRESPONSE._serialized_end=172
  _READYREQUEST._serialized_start=174
  _READYREQUEST._serialized_end=221
  _READYRESPONSE._serialized_start=223
  _READYRESPONSE._serialized_end=285
  _PLAYREQUEST._serialized_start=287
  _PLAYREQUEST._serialized_end=333
  _GAMESTATUSRESPONSE._serialized_start=335
  _GAMESTATUSRESPONSE._serialized_end=422
  _WINCHECKREQUEST._serialized_start=424
  _WINCHECKREQUEST._serialized_end=474
  _WINCHECKRESPONSE._serialized_start=476
  _WINCHECKRESPONSE._serialized_end=527
  _BINGO._serialized_start=530
  _BINGO._serialized_end=761
# @@protoc_insertion_point(module_scope)
