# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: intersection.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.transit import gtfs_realtime_pb2 as gtfs__realtime__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='intersection.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x12intersection.proto\x1a\x13gtfs-realtime.proto\"\xfe\x01\n\x16IntersectionTripUpdate\x12\x10\n\x08headsign\x18\x01 \x01(\t\x12\x18\n\x10route_short_name\x18\x02 \x01(\t\x12\x17\n\x0froute_long_name\x18\x03 \x01(\t\x12\x13\n\x0broute_color\x18\x04 \x01(\t\x12\x18\n\x10route_text_color\x18\x05 \x01(\t\x12\x10\n\x08\x62lock_id\x18\x06 \x01(\t\x12\x17\n\x0f\x61gency_timezone\x18\x07 \x01(\t\x12\x15\n\rcustom_status\x18\x08 \x01(\t\x12\x1a\n\x12scheduled_interval\x18\t \x01(\x05\x12\x12\n\nroute_icon\x18\n \x01(\t\"\xce\x01\n\x1aIntersectionStopTimeUpdate\x12\r\n\x05track\x18\x01 \x01(\t\x12\x45\n\x11scheduled_arrival\x18\x02 \x01(\x0b\x32*.transit_realtime.TripUpdate.StopTimeEvent\x12G\n\x13scheduled_departure\x18\x03 \x01(\x0b\x32*.transit_realtime.TripUpdate.StopTimeEvent\x12\x11\n\tstop_name\x18\x04 \x01(\t\"3\n\x1dIntersectionVehicleDescriptor\x12\x12\n\nrun_number\x18\x01 \x01(\t:X\n\x18intersection_trip_update\x12\x1c.transit_realtime.TripUpdate\x18\xc3\x0f \x01(\x0b\x32\x17.IntersectionTripUpdate:p\n\x1dintersection_stop_time_update\x12+.transit_realtime.TripUpdate.StopTimeUpdate\x18\xc3\x0f \x01(\x0b\x32\x1b.IntersectionStopTimeUpdate:m\n\x1fintersection_vehicle_descriptor\x12#.transit_realtime.VehicleDescriptor\x18\xc3\x0f \x01(\x0b\x32\x1e.IntersectionVehicleDescriptor'
  ,
  dependencies=[gtfs__realtime__pb2.DESCRIPTOR,])


INTERSECTION_TRIP_UPDATE_FIELD_NUMBER = 1987
intersection_trip_update = _descriptor.FieldDescriptor(
  name='intersection_trip_update', full_name='intersection_trip_update', index=0,
  number=1987, type=11, cpp_type=10, label=1,
  has_default_value=False, default_value=None,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key)
INTERSECTION_STOP_TIME_UPDATE_FIELD_NUMBER = 1987
intersection_stop_time_update = _descriptor.FieldDescriptor(
  name='intersection_stop_time_update', full_name='intersection_stop_time_update', index=1,
  number=1987, type=11, cpp_type=10, label=1,
  has_default_value=False, default_value=None,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key)
INTERSECTION_VEHICLE_DESCRIPTOR_FIELD_NUMBER = 1987
intersection_vehicle_descriptor = _descriptor.FieldDescriptor(
  name='intersection_vehicle_descriptor', full_name='intersection_vehicle_descriptor', index=2,
  number=1987, type=11, cpp_type=10, label=1,
  has_default_value=False, default_value=None,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key)


_INTERSECTIONTRIPUPDATE = _descriptor.Descriptor(
  name='IntersectionTripUpdate',
  full_name='IntersectionTripUpdate',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='headsign', full_name='IntersectionTripUpdate.headsign', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='route_short_name', full_name='IntersectionTripUpdate.route_short_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='route_long_name', full_name='IntersectionTripUpdate.route_long_name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='route_color', full_name='IntersectionTripUpdate.route_color', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='route_text_color', full_name='IntersectionTripUpdate.route_text_color', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='block_id', full_name='IntersectionTripUpdate.block_id', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='agency_timezone', full_name='IntersectionTripUpdate.agency_timezone', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='custom_status', full_name='IntersectionTripUpdate.custom_status', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='scheduled_interval', full_name='IntersectionTripUpdate.scheduled_interval', index=8,
      number=9, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='route_icon', full_name='IntersectionTripUpdate.route_icon', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=44,
  serialized_end=298,
)


_INTERSECTIONSTOPTIMEUPDATE = _descriptor.Descriptor(
  name='IntersectionStopTimeUpdate',
  full_name='IntersectionStopTimeUpdate',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='track', full_name='IntersectionStopTimeUpdate.track', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='scheduled_arrival', full_name='IntersectionStopTimeUpdate.scheduled_arrival', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='scheduled_departure', full_name='IntersectionStopTimeUpdate.scheduled_departure', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='stop_name', full_name='IntersectionStopTimeUpdate.stop_name', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=301,
  serialized_end=507,
)


_INTERSECTIONVEHICLEDESCRIPTOR = _descriptor.Descriptor(
  name='IntersectionVehicleDescriptor',
  full_name='IntersectionVehicleDescriptor',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='run_number', full_name='IntersectionVehicleDescriptor.run_number', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=509,
  serialized_end=560,
)

_INTERSECTIONSTOPTIMEUPDATE.fields_by_name['scheduled_arrival'].message_type = gtfs__realtime__pb2._TRIPUPDATE_STOPTIMEEVENT
_INTERSECTIONSTOPTIMEUPDATE.fields_by_name['scheduled_departure'].message_type = gtfs__realtime__pb2._TRIPUPDATE_STOPTIMEEVENT
DESCRIPTOR.message_types_by_name['IntersectionTripUpdate'] = _INTERSECTIONTRIPUPDATE
DESCRIPTOR.message_types_by_name['IntersectionStopTimeUpdate'] = _INTERSECTIONSTOPTIMEUPDATE
DESCRIPTOR.message_types_by_name['IntersectionVehicleDescriptor'] = _INTERSECTIONVEHICLEDESCRIPTOR
DESCRIPTOR.extensions_by_name['intersection_trip_update'] = intersection_trip_update
DESCRIPTOR.extensions_by_name['intersection_stop_time_update'] = intersection_stop_time_update
DESCRIPTOR.extensions_by_name['intersection_vehicle_descriptor'] = intersection_vehicle_descriptor
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

IntersectionTripUpdate = _reflection.GeneratedProtocolMessageType('IntersectionTripUpdate', (_message.Message,), {
  'DESCRIPTOR' : _INTERSECTIONTRIPUPDATE,
  '__module__' : 'intersection_pb2'
  # @@protoc_insertion_point(class_scope:IntersectionTripUpdate)
  })
_sym_db.RegisterMessage(IntersectionTripUpdate)

IntersectionStopTimeUpdate = _reflection.GeneratedProtocolMessageType('IntersectionStopTimeUpdate', (_message.Message,), {
  'DESCRIPTOR' : _INTERSECTIONSTOPTIMEUPDATE,
  '__module__' : 'intersection_pb2'
  # @@protoc_insertion_point(class_scope:IntersectionStopTimeUpdate)
  })
_sym_db.RegisterMessage(IntersectionStopTimeUpdate)

IntersectionVehicleDescriptor = _reflection.GeneratedProtocolMessageType('IntersectionVehicleDescriptor', (_message.Message,), {
  'DESCRIPTOR' : _INTERSECTIONVEHICLEDESCRIPTOR,
  '__module__' : 'intersection_pb2'
  # @@protoc_insertion_point(class_scope:IntersectionVehicleDescriptor)
  })
_sym_db.RegisterMessage(IntersectionVehicleDescriptor)

intersection_trip_update.message_type = _INTERSECTIONTRIPUPDATE
gtfs__realtime__pb2.TripUpdate.RegisterExtension(intersection_trip_update)
intersection_stop_time_update.message_type = _INTERSECTIONSTOPTIMEUPDATE
gtfs__realtime__pb2.TripUpdate.StopTimeUpdate.RegisterExtension(intersection_stop_time_update)
intersection_vehicle_descriptor.message_type = _INTERSECTIONVEHICLEDESCRIPTOR
gtfs__realtime__pb2.VehicleDescriptor.RegisterExtension(intersection_vehicle_descriptor)

# @@protoc_insertion_point(module_scope)
