import json
from collections import defaultdict

import pendulum

from gtfs_realtime_translators.factories import TripUpdate, FeedMessage


class MbtaGtfsRealtimeTranslator:
    TIMEZONE = 'America/New_York'

    def __call__(self, data):
        json_data = json.loads(data)
        predictions = json_data['data']
        included = json_data['included']
        static_data = self.__get_static_data(included)
        entities = self.__make_trip_updates(predictions, static_data)
        return FeedMessage.create(entities=entities)

    @classmethod
    def __to_unix_time(cls, time):
        return pendulum.parse(time).in_tz(cls.TIMEZONE).int_timestamp

    @classmethod
    def __get_static_data(cls, included):
        static_data = defaultdict(dict)
        for relationship in included:
            relationship_type = relationship['type']
            static_data_type = StaticDataTypeRegistry.get(relationship_type)
            if static_data_type is not None:
                static_data[static_data_type.NAME][relationship['id']] = \
                    static_data_type.create_entry(relationship['attributes'],
                                                  static_data_type.KEYS)

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

            # route fields
            route_color = static_data['routes'][route_id]['color']
            route_text_color = static_data['routes'][route_id]['text_color']
            route_long_name = static_data['routes'][route_id]['long_name']
            route_short_name = static_data['routes'][route_id]['short_name']

            # scheduled times
            schedule_id = relationships['schedule']['data']['id']
            scheduled_arrival_time = static_data['schedules'][schedule_id]['arrival_time']
            scheduled_departure_time = static_data['schedules'][schedule_id]['departure_time']

            stop_name = static_data['stops'][stop_id]['stop_name']
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


class StaticData:

    def create_entry(self, attributes, keys):
        return {key: attributes[key] for key in keys}


class Route(StaticData):
    NAME = 'routes'
    KEYS = ['color', 'text_color', 'long_name', 'short_name']


class Stop(StaticData):
    NAME = 'stops'
    KEYS = ['name']


class Schedule(StaticData):
    NAME = 'schedules'
    KEYS = ['arrival_time', 'departure_time']


class Trip(StaticData):
    NAME = 'trips'
    KEYS = ['headsign']


class StaticDataTypeRegistry:
    TYPES = {'route': Route, 'stop': Stop, 'schedule': Schedule, 'trip': Trip}

    @staticmethod
    def get(key):
        return StaticDataTypeRegistry.TYPES.get(key)
