import json

import pendulum

from gtfs_realtime_translators.factories import TripUpdate, FeedMessage


class CtaBusGtfsRealtimeTranslator:
    TIMEZONE = 'America/Chicago'

    def __call__(self, data):
        json_data = json.loads(data)
        try:
            predictions = json_data['bustime-response']['prd']
        except Exception:
            predictions = []

        entities = [self.__make_trip_update(idx, arr) for idx, arr in enumerate(predictions)]

        return FeedMessage.create(entities=entities)


    @classmethod
    def __to_unix_time(cls, time):
        return pendulum.parse(time).in_tz(cls.TIMEZONE).int_timestamp

    @classmethod
    def __make_trip_update(cls, _id, prediction):
        entity_id = str(_id + 1)
        route_id = prediction['rt']
        stop_id = prediction['stpid']

        # Per the docs, the prediction is either for a scheduled departure, or realtime arrival
        departure_type = 'D'
        is_scheduled = prediction['typ'] == departure_type

        parsed_arrival_time = cls.__to_unix_time(prediction['prdtm'])
        arrival_time = None if is_scheduled else parsed_arrival_time

        ##### Intersection Extensions
        headsign = prediction['des']
        scheduled_arrival_time = parsed_arrival_time if is_scheduled else None

        return TripUpdate.create(entity_id=entity_id,
                                route_id=route_id,
                                stop_id=stop_id,
                                arrival_time=arrival_time,
                                headsign=headsign,
                                scheduled_arrival_time=scheduled_arrival_time)
