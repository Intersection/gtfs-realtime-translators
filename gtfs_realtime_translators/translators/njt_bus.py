import pendulum
import xmltodict
import datetime
from gtfs_realtime_translators.factories import FeedMessage, TripUpdate


class NjtBusGtfsRealtimeTranslator:

    TIMEZONE = 'America/New_York'

    def __call__(self, data):
        station_data = xmltodict.parse(data)
        entities = self.__make_trip_updates(station_data)
        return FeedMessage.create(entities=entities)

    @classmethod
    def __to_unix_time(cls, time):
        dt = pendulum.from_format(
            time, 'MM/DD/YYYY HH:mm:ss A', tz=cls.TIMEZONE).in_tz('UTC')
        return dt

    @classmethod
    def __replace_time(cls, sched_dep_time, new_time):
        dtime = pendulum.from_format(new_time, 'HH:mm:ss', tz=cls.TIMEZONE)
        hour = dtime.hour
        minute = dtime.minute
        second = dtime.second
        dt = pendulum.from_format(
            sched_dep_time, 'MM/DD/YYYY HH:mm:ss A', tz=cls.TIMEZONE)
        dt = dt.replace(hour=hour, minute=minute, second=second)
        dt = dt.in_tz('UTC')
        return dt

    @classmethod
    def __make_trip_updates(cls, data):
        trip_updates = []
        trips = data['NEXTTRIPROWSET'].values()

        for value in trips:
            for idx, item_entry in enumerate(value):
                # Intersection Extensions
                headsign = item_entry['header']
                stop_id = item_entry['stop_id']
                stop_name = item_entry['stop_name']
                trip_id = item_entry['Trip_id']
                route_id = item_entry['route']
                scheduled_datetime = cls.__to_unix_time(
                    item_entry['sched_dep_time'])
                arrival_time = int(cls.__replace_time(
                    item_entry['sched_dep_time'], item_entry['arrival_time']).timestamp())
                departure_time = int(cls.__replace_time(
                    item_entry['sched_dep_time'], item_entry['arrival_time']).timestamp())
                scheduled_departure_time = int(scheduled_datetime.timestamp())

                trip_update = TripUpdate.create(entity_id=str(idx + 1),
                                                route_id=route_id,
                                                trip_id=trip_id,
                                                stop_id=stop_id,
                                                stop_name=stop_name,
                                                headsign=headsign,
                                                departure_time=departure_time,
                                                arrival_time=arrival_time,
                                                scheduled_departure_time=scheduled_departure_time,
                                                scheduled_arrival_time=scheduled_departure_time,
                                                agency_timezone=cls.TIMEZONE)
                trip_updates.append(trip_update)

        return trip_updates
