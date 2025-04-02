import json

import pendulum

from gtfs_realtime_translators.factories import TripUpdate, FeedMessage


class MartaRailGtfsRealtimeTranslator:
    TIMEZONE = 'America/New_York'

    LINE_ROUTE_DATA_MAP = {
        'BLUE': ('BLUE', 'Blue Line', '0075B2', 'FFFFFF'),
        'GOLD': ('GOLD', 'Gold Line', 'D4A723', '000000'),
        'GREEN': ('GREEN', 'Green Line', '009D4B', '000000'),
        'RED': ('RED', 'Red Line', 'CE242B', 'FFFFFF'),
    }

    LINE_STATION_DESTINATION_STOP_ID_MAP = {
        ('GOLD', 'LINDBERGH STATION', 'DORAVILLE'): '58',
        ('GOLD', 'LINDBERGH STATION', 'AIRPORT'): '57',
        ('RED', 'LINDBERGH STATION', 'NORTH SPRINGS'): '999549',
        ('RED', 'LINDBERGH STATION', 'AIRPORT'): '999549',
        ('RED', 'LINDBERGH STATION', 'LINDBERGH'): '999690',
    }

    def __call__(self, data):
        predictions = json.loads(data)
        entities = []
        current_date = pendulum.today(self.TIMEZONE).format('YYYY-MM-DD')
        for index, prediction in enumerate(predictions):
            entities.append(self.__make_trip_update(index,
                                                    prediction,
                                                    current_date))

        return FeedMessage.create(entities=entities)

    @classmethod
    def __make_trip_update(cls, _id, prediction, current_date):
        entity_id = str(_id + 1)
        vehicle_id = prediction.get('TRAIN_ID')
        stop_name = prediction.get('STATION')
        headsign = prediction.get('DESTINATION')
        custom_status = prediction.get('WAITING_TIME')
        station = prediction.get('STATION')
        line = prediction.get('LINE')

        route_data = cls.__get_route_data(line)
        route_short_name = route_data[0]
        route_long_name = route_data[1]
        route_color = route_data[2]
        route_text_color = route_data[3]

        stop_id = cls.__get_stop_id(line, station, headsign)

        unix_arrival_time = cls.__to_unix_time(prediction.get('NEXT_ARR'),
                                               current_date)
        is_realtime = prediction.get('IS_REALTIME')

        arrival_time = unix_arrival_time if is_realtime else None
        scheduled_arrival_time = None if is_realtime else unix_arrival_time

        return TripUpdate.create(entity_id=entity_id,
                                 route_short_name=route_short_name,
                                 route_long_name=route_long_name,
                                 route_color=route_color,
                                 route_text_color=route_text_color,
                                 stop_id=stop_id,
                                 vehicle_id=vehicle_id,
                                 stop_name=stop_name,
                                 headsign=headsign,
                                 custom_status=custom_status,
                                 arrival_time=arrival_time,
                                 scheduled_arrival_time=scheduled_arrival_time,
                                 agency_timezone=cls.TIMEZONE)

    @classmethod
    def __get_route_data(cls, line):
        return cls.LINE_ROUTE_DATA_MAP.get(line)

    @classmethod
    def __get_stop_id(cls, line, station, headsign):
        return cls.LINE_STATION_DESTINATION_STOP_ID_MAP.get((line.upper(),
                                                             station.upper(),
                                                             headsign.upper()))

    @classmethod
    def __to_unix_time(cls, time, current_date):
        datetime_str = f"{current_date} {time}"
        dt = pendulum.from_format(datetime_str,
                                  'YYYY-MM-DD h:mm:ss A',
                                  tz=cls.TIMEZONE).in_tz('UTC')
        return dt.int_timestamp
