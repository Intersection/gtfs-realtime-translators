import json
import warnings

from collections import defaultdict

import pendulum

from gtfs_realtime_translators.factories import TripUpdate, FeedMessage


class MbtaGtfsRealtimeTranslator:
    TIMEZONE = 'America/New_York'

    def __call__(self, data):
        json_data = json.loads(data)
        predictions = json_data['data']
        static_relationships = json_data['included']
        static_data = self.__get_static_data(static_relationships)
        entities = self.__make_trip_updates(predictions, static_data)
        return FeedMessage.create(entities=entities)

    @classmethod
    def __to_unix_time(cls, time):
        return pendulum.parse(time).in_tz(cls.TIMEZONE).int_timestamp

    @classmethod
    def __get_static_data(cls, static_relationships):
        static_data = defaultdict(dict)
        for entity in static_relationships:
            entity_type = entity['type']
            static_data_type = StaticDataTypeRegistry.get(entity_type)
            static_data[static_data_type.NAME][entity['id']] = \
                static_data_type.create_entry(entity['id'],
                                              entity['attributes'],
                                              static_data_type.FIELDS)
        return static_data

    @classmethod
    def __make_trip_updates(cls, predictions, static_data):
        trip_updates = []
        for idx, prediction in enumerate(predictions):
            entity_id = str(idx + 1)
            relationships = prediction['relationships']
            attributes = prediction['attributes']
            stop_id = relationships['stop']['data']['id']
            route_id = relationships['route']['data']['id']
            trip_id = relationships['trip']['data']['id']
            raw_arrival_time = attributes['arrival_time']
            raw_departure_time = attributes['departure_time']
            direction_id = attributes['direction_id']
            scheduled_arrival_time = None
            scheduled_departure_time = None

            # route fields
            route_color = static_data['routes'][route_id]['color']
            route_text_color = static_data['routes'][route_id]['text_color']
            route_long_name = static_data['routes'][route_id]['long_name']
            route_short_name = static_data['routes'][route_id]['short_name']

            # scheduled times
            if relationships['schedule']['data'] is not None:
                schedule_id = relationships['schedule']['data']['id']
                scheduled_arrival_time = \
                    static_data['schedules'][schedule_id]['arrival_time']
                scheduled_departure_time = \
                    static_data['schedules'][schedule_id]['departure_time']

            stop_name = static_data['stops'][stop_id]['name']
            headsign = static_data['trips'][trip_id]['headsign']

            if cls.__should_capture_prediction(raw_departure_time):
                arrival_time, departure_time = cls.__set_arrival_and_departure_times(
                    raw_arrival_time, raw_departure_time)
                trip_update = TripUpdate.create(
                    entity_id=entity_id,
                    route_id=route_id,
                    stop_id=stop_id,
                    trip_id=trip_id,
                    arrival_time=arrival_time,
                    departure_time=departure_time,
                    direction_id=direction_id,
                    route_color=route_color,
                    route_text_color=route_text_color,
                    route_long_name=route_long_name,
                    route_short_name=route_short_name,
                    scheduled_arrival_time=scheduled_arrival_time,
                    scheduled_departure_time=scheduled_departure_time,
                    stop_name=stop_name,
                    headsign=headsign,
                    agency_timezone=cls.TIMEZONE
                )
                trip_updates.append(trip_update)

        return trip_updates

    @classmethod
    def __set_arrival_and_departure_times(cls, raw_arrival_time, raw_departure_time):
        departure_time = cls.__to_unix_time(
            raw_departure_time)
        if raw_arrival_time:
            arrival_time = cls.__to_unix_time(
                raw_arrival_time)
        else:
            arrival_time = departure_time
        return arrival_time, departure_time

    @classmethod
    def __should_capture_prediction(cls, raw_departure_time):
        return raw_departure_time


class RouteShortNameTranslate:
    ROUTE_ID_SHORT_NAMES = {
        'Green-B': 'GL·B',
        'Green-C': 'GL·C',
        'Green-D': 'GL·D',
        'Green-E': 'GL·E',
        'Blue': 'BL',
        'Red': 'RL',
        'Orange': 'OL',
        'Mattapan': 'M'
    }

    def __call__(self, attributes_map, field, entity_id):
        if entity_id in self.ROUTE_ID_SHORT_NAMES:
            return self.ROUTE_ID_SHORT_NAMES.get(entity_id)
        if attributes_map['type'] == '2':
            return attributes_map[field].replace(' Line', '')


class IdentityTranslate:

    def __call__(self, attributes_map, field, entity_id):
        return attributes_map[field]


class StaticData:
    """
    Represents a static data `type` from the MBTA API response. Implements
    the create_entry() interface. Each instance should contain:
        NAME: the key in the map that we create from the static data in the
            MBTA API response
        FIELDS: the list of fields that we want to extract from the MBTA API
            response
        FIELD_TRANSLATORS: optional map of fields to their translators
    """
    def create_entry(self, entity_id, attributes_map, fields):
        """
        Extracts into a map a subset of the fields from the attributes map
        contained within each entity in the MBTA API response.
        """
        entry = {}
        for field in fields:
            field_translate = self.get_field_translator(field)
            if field_translate is not None:
                value = field_translate(attributes_map,
                                        field,
                                        entity_id)
            else:
                value = attributes_map[field]
            entry[field] = value
        return entry

    def get_field_translator(self, field):
        if not hasattr(self, 'FIELD_TRANSLATORS'):
            return IdentityTranslate()
        return self.FIELD_TRANSLATORS.get(field, IdentityTranslate())


class Route(StaticData):
    NAME = 'routes'
    FIELDS = ['color', 'text_color', 'long_name', 'short_name']
    FIELD_TRANSLATORS = {
        'short_name': RouteShortNameTranslate()
    }


class Stop(StaticData):
    NAME = 'stops'
    FIELDS = ['name']


class Schedule(StaticData):
    NAME = 'schedules'
    FIELDS = ['arrival_time', 'departure_time']


class Trip(StaticData):
    NAME = 'trips'
    FIELDS = ['headsign']


class StaticDataTypeWarning(Warning):
    pass


class StaticDataTypeRegistry:
    """
    This a map of the possible values in the `type` field and their
    corresponding class representations.
    """
    TYPES = {'route': Route(), 'stop': Stop(), 'schedule': Schedule(),
             'trip': Trip()}

    @classmethod
    def get(cls, key):
        if key in cls.TYPES:
            return cls.TYPES[key]
        else:
            warnings.warn(f'No static data type defined for entity type {key}',
                          StaticDataTypeWarning)
