import json

import pendulum

from gtfs_realtime_translators.factories import TripUpdate, FeedMessage


class MbtaGtfsRealtimeTranslator:
    TIMEZONE = 'America/New_York'

    def __call__(self, data):
        json_data = json.loads(data)
        predictions = json_data['data']
        entities = self.__make_trip_updates(predictions)
        return FeedMessage.create(entities=entities)

    @classmethod
    def __to_unix_time(cls, time):
        return pendulum.parse(time).in_tz(cls.TIMEZONE).int_timestamp

    @classmethod
    def __make_trip_updates(cls, predictions):
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

            if cls.__should_capture_prediction(raw_arrival_time, raw_departure_time):
                arrival_time, departure_time = cls.__set_arrival_and_departure_times(
                    raw_arrival_time, raw_departure_time)
                trip_update = TripUpdate.create(
                    entity_id=entity_id,
                    route_id=route_id,
                    stop_id=stop_id,
                    trip_id=trip_id,
                    arrival_time=arrival_time,
                    departure_time=departure_time
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
