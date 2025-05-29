import json

import pendulum

from gtfs_realtime_translators.factories import TripUpdate, FeedMessage


class CtaBusGtfsRealtimeTranslator:
    TIMEZONE = 'America/Chicago'

    def __call__(self, data):
        json_data = json.loads(data)
        predictions = json_data.get('bustime-response', {}).get('prd', [])
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
        stop_name = prediction['stpnm']
        trip_id = prediction['tatripid']

        arrival_time = cls.__to_unix_time(prediction['prdtm'])

        ##### Intersection Extensions
        headsign = prediction['des']
        custom_status = cls.__get_custom_status(prediction['dyn'],
                                                prediction['dly'],
                                                prediction['prdctdn'])

        return TripUpdate.create(entity_id=entity_id,
                                 route_id=route_id,
                                 stop_id=stop_id,
                                 stop_name=stop_name,
                                 trip_id=trip_id,
                                 arrival_time=arrival_time,
                                 headsign=headsign,
                                 custom_status=custom_status,
                                 agency_timezone=cls.TIMEZONE)

    @classmethod
    def __get_custom_status(cls, dynamic_action_type, delay, prediction_time):
        if dynamic_action_type == 1:
            return 'CANCELED'
        if dynamic_action_type == 4:
            return 'EXPRESSED'

        if delay:
            return 'DELAYED'

        if not prediction_time:
            return None
        elif prediction_time == 'DUE':
            return prediction_time
        return f'{prediction_time} min'
