import pendulum
from datetime import datetime

from gtfs_realtime_translators.factories import FeedMessage, TripUpdate
import json


class NjtBusJsonGtfsRealtimeTranslator:

    TIMEZONE = 'America/New_York'

    DEFAULT_ROUTE_COLOR = '6C6D71'
    DEFAULT_ROUTE_TEXT_COLOR = 'FFFFFF'

    def __init__(self, **kwargs):
        self.stop_id = kwargs.get('stop_id')

    def __call__(self, data):
        data = json.loads(data)
        items = data.get('DVTrip', [])
            
        entities = self.__make_trip_updates(items, self.stop_id)
        return FeedMessage.create(entities=entities)

    @classmethod
    def __make_trip_updates(cls, items, stop_id):
        trip_updates = []
        
        for index, item in enumerate(items):
            route_short_name = item.get('public_route', '')
            headsign = item.get('header', '')
            track = item.get('lanegate', '')
            
            departure_time_str = item.get('departuretime', '')
            scheduled_departure_str = item.get('sched_dep_time', '')
            
            departure_time = cls.__time_to_unix_time(departure_time_str)
            scheduled_departure_time = cls.__time_to_unix_time(scheduled_departure_str)
            
            arrival_time = departure_time
            scheduled_arrival_time = scheduled_departure_time

            trip_update = TripUpdate.create(
                entity_id=str(index + 1),
                stop_id=stop_id,
                departure_time=departure_time,
                scheduled_departure_time=scheduled_departure_time,
                arrival_time=arrival_time,
                scheduled_arrival_time=scheduled_arrival_time,
                route_short_name=route_short_name,
                route_color=cls.DEFAULT_ROUTE_COLOR,
                route_text_color=cls.DEFAULT_ROUTE_TEXT_COLOR,
                headsign=headsign,
                track=track,
                agency_timezone=cls.TIMEZONE,
            )
            
            trip_updates.append(trip_update)

        return trip_updates

    @classmethod
    def __time_to_unix_time(cls, time_str):
        """
        Tries to parse a datetime string as either:
        - 'M/D/YYYY h:mm:ss A'
        - 'h:mm A' (uses today's date)

        Returns: Unix timestamp (int)
        """
        time_str = time_str.strip()

        try:
            dt = pendulum.from_format(time_str, "M/D/YYYY h:mm:ss A",
                                      tz=cls.TIMEZONE)
        except Exception as e:
            today = pendulum.today(tz=cls.TIMEZONE).to_date_string()
            dt = pendulum.from_format(f"{today} {time_str}",
                                      "YYYY-MM-DD h:mm A",
                                      tz=cls.TIMEZONE)

        return dt.int_timestamp
