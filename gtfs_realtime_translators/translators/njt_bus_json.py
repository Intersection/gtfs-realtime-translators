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
    def __parse_time_to_unix(cls, time_str):
        """
        Parse time string to Unix timestamp.
        Handles formats like "01:40 PM" and "7/25/2025 1:40:00 PM"
        """
        try:
            # Try parsing full datetime format first
            if '/' in time_str:
                dt = datetime.strptime(time_str, '%m/%d/%Y %I:%M:%S %p')
                # Convert to pendulum with timezone
                pdt = pendulum.instance(dt, tz=cls.TIMEZONE)
                return int(pdt.timestamp())
            else:
                # For time-only format, use current date
                current_date = pendulum.now(cls.TIMEZONE).format('YYYY-MM-DD')
                full_datetime_str = f"{current_date} {time_str}"
                dt = datetime.strptime(full_datetime_str, '%Y-%m-%d %I:%M %p')
                pdt = pendulum.instance(dt, tz=cls.TIMEZONE)
                return int(pdt.timestamp())
        except ValueError:
            # If parsing fails, return current timestamp
            return int(pendulum.now(cls.TIMEZONE).timestamp())

    @classmethod
    def __make_trip_updates(cls, items, stop_id):
        trip_updates = []
        
        for index, item in enumerate(items):
            route_short_name = item.get('public_route', '')
            headsign = item.get('header', '')
            track = item.get('lanegate', '')
            
            departure_time_str = item.get('departuretime', '')
            scheduled_departure_str = item.get('sched_dep_time', '')
            
            departure_time = cls.__parse_time_to_unix(departure_time_str)
            scheduled_departure_time = cls.__parse_time_to_unix(scheduled_departure_str)
            
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

