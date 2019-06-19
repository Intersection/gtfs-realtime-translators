import re
import copy

import pendulum

from gtfs_realtime_translators.factories import TripUpdate, FeedMessage


class SeptaRegionalRailTranslator:
    TIMEZONE = 'America/New_York'
    STATUS_PATTERN = re.compile(r'(?P<delay>\d*) min')
    ROUTE_ID_LOOKUP = {
        'Airport': 'AIR',
        'Chestnut Hill East': 'CHE',
        'Chestnut Hill West': 'CHW',
        'Lansdale/Doylestown': 'LAN',
        'Media/Elwyn': 'MED',
        'Fox Chase': 'FOX',
        'Manayunk/Norristown': 'NOR',
        'Paoli/Thorndale': 'PAO',
        'Cynwyd': 'CYN',
        'Trenton': 'TRE',
        'Warminster': 'WAR',
        'Wilmington/Newark': 'WIL',
        'West Trenton': 'WTR',
    }

    def __init__(self, data, **kwargs):
        stop_id = kwargs['stop_id']
        filter_seconds = kwargs.get('filter_seconds', 10800) # default 10800s => 3hrs
        latest_valid_time = self.calculate_time_at(seconds=filter_seconds)

        root_key = next(iter([*data]), None)

        if root_key is None:
            raise ValueError('root_key: unexpected format')
        
        arrivals_body = data[root_key]
        northbound = [ direction_list['Northbound'] for direction_list in arrivals_body if [*direction_list][0] == 'Northbound' ][0]
        southbound = [ direction_list['Southbound'] for direction_list in arrivals_body if [*direction_list][0] == 'Southbound' ][0]
        arrivals = northbound + southbound

        transformed_arrivals = [ self.transform_arrival(arrival) for arrival in arrivals ]
        filtered_arrivals = [ arrival for arrival in transformed_arrivals if arrival['sched_time'] <= latest_valid_time ]

        entities = [ self.__make_trip_update(idx, stop_id, arrival) for idx, arrival in enumerate(filtered_arrivals) ]
        self.feed_message = FeedMessage.create(entities=entities)

    @classmethod
    def calculate_time_at(cls, **kwargs):
        now = pendulum.now()
        future_time = now.add(**kwargs)
        return int(future_time.timestamp())

    @classmethod
    def to_unix_timestamp(cls, time):
        time_obj = pendulum.parse(time, tz=cls.TIMEZONE)
        return int(time_obj.timestamp())

    @classmethod
    def transform_arrival(cls, arrival):
        transformed_arrival = copy.deepcopy(arrival)

        transformed_arrival['sched_time'] = cls.to_unix_timestamp(arrival['sched_time'])
        transformed_arrival['depart_time'] = cls.to_unix_timestamp(arrival['depart_time'])

        return transformed_arrival

    @classmethod
    def calculate_realtime(cls, time, status):
        matches = cls.STATUS_PATTERN.search(status)

        # If we do not see the pattern '<num> min', this train is considered On Time
        if matches is None:
            return time

        delay_in_minutes = int(matches.group('delay'))
        return int((pendulum.from_timestamp(time).add(minutes=delay_in_minutes)).timestamp())

    @classmethod
    def __make_trip_update(cls, _id, stop_id, arrival):
        entity_id = str(_id + 1)
        route_id = cls.ROUTE_ID_LOOKUP.get(arrival['line'], None)
        arrival_time = cls.calculate_realtime(arrival['sched_time'], arrival['status'])
        departure_time = cls.calculate_realtime(arrival['depart_time'], arrival['status'])

        return TripUpdate.create(entity_id=entity_id,
                                 arrival_time=arrival_time,
                                 departure_time=departure_time,
                                 stop_id=stop_id,
                                 route_id=route_id,
                                 scheduled_arrival_time=arrival['sched_time'],
                                 scheduled_departure_time=arrival['depart_time'],
                                 track=arrival['track'],
                                 headsign=arrival['destination'])

    def serialize(self):
        return self.feed_message.SerializeToString()
