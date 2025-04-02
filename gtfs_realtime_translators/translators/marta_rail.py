import json

import pendulum

from gtfs_realtime_translators.factories import TripUpdate, FeedMessage


class MartaRailGtfsRealtimeTranslator:
    TIMEZONE = 'America/New_York'

    LINE_ROUTE_ID_MAP = {
        'BLUE': '24548',
        'GOLD': '24549',
        'GREEN': '24550',
        'RED': '24551'
    }

    ARRIVAL_TIME_FORMAT = 'MM/DD/YYYY h:mm:ss A'

    def __call__(self, data):
        predictions = json.loads(data)
        entities = []
        for index, prediction in enumerate(predictions):
            entities.append(self.__make_trip_update(index, prediction))

        return FeedMessage.create(entities=entities)

    @classmethod
    def __make_trip_update(cls, _id, prediction):
        entity_id = str(_id + 1)
        route_id = cls.__get_route_id(prediction.get('LINE'))
        vehicle_id = prediction.get('TRAIN_ID')
        stop_name = prediction.get('STATION')
        headsign = prediction.get('DESTINATION')
        custom_status = prediction.get('WAITING_TIME')

        is_realtime = prediction.get('IS_REALTIME')
        next_arr = prediction.get('NEXT_ARR')

        arrival_time = None
        scheduled_arrival_time = None

        if is_realtime:
            arrival_time = cls.__to_unix_time(next_arr)
        else:
            scheduled_arrival_time = cls.__to_unix_time(next_arr)

        return TripUpdate.create(entity_id=entity_id,
                                 route_id=route_id,
                                 vehicle_id=vehicle_id,
                                 stop_name=stop_name,
                                 headsign=headsign,
                                 custom_status=custom_status,
                                 arrival_time=arrival_time,
                                 scheduled_arrival_time=scheduled_arrival_time,
                                 agency_timezone=cls.TIMEZONE)

    @classmethod
    def __get_route_id(cls, line):
        return cls.LINE_ROUTE_ID_MAP.get(line)

    @classmethod
    def __to_unix_time(cls, time):
        dt = pendulum.from_format(time,
                                  cls.ARRIVAL_TIME_FORMAT,
                                  tz=cls.TIMEZONE)
        return dt.int_timestamp
