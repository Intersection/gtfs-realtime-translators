import json
import re
import copy

import pendulum

from gtfs_realtime_translators.factories import TripUpdate, FeedMessage
from gtfs_realtime_translators.validators import RequiredFieldValidator


class SeptaRegionalRailTranslator:
    TIMEZONE = 'America/New_York'
    STATUS_PATTERN = re.compile(r'(?P<delay>\d*) min')
    ROUTE_ID_LOOKUP = {
        'Airport': 'AIR',
        'Chestnut Hill East': 'CHE',
        'Chestnut Hill West': 'CHW',
        'Lansdale/Doylestown': 'LAN',
        'Media/Wawa': 'MED',
        'Fox Chase': 'FOX',
        'Manayunk/Norristown': 'NOR',
        'Paoli/Thorndale': 'PAO',
        'Cynwyd': 'CYN',
        'Trenton': 'TRE',
        'Warminster': 'WAR',
        'Wilmington/Newark': 'WIL',
        'West Trenton': 'WTR',
    }

    def __init__(self, **kwargs):
        self.stop_id = kwargs.get('stop_id')
        RequiredFieldValidator.validate_field_value('stop_id', self.stop_id)
        filter_seconds = kwargs.get('filter_seconds', 10800) # default 10800s => 3hrs
        self.latest_valid_time = self.calculate_time_at(seconds=filter_seconds)

    def __call__(self, data):
        json_data = json.loads(data)
        root_key = next(iter([*json_data]), None)

        if root_key is None:
            raise ValueError('root_key: unexpected format')
        
        arrivals_body = json_data[root_key]
        northbound = self.get_arrivals_from_direction_list('Northbound', arrivals_body)
        southbound = self.get_arrivals_from_direction_list('Southbound', arrivals_body)
        arrivals = northbound + southbound

        transformed_arrivals = [ self.transform_arrival(arrival) for arrival in arrivals ]
        filtered_arrivals = [ arrival for arrival in transformed_arrivals if arrival['sched_time'] <= self.latest_valid_time ]

        entities = [ self.__make_trip_update(idx, self.stop_id, arrival) for idx, arrival in enumerate(filtered_arrivals) ]
        return FeedMessage.create(entities=entities)

    @classmethod
    def get_arrivals_from_direction_list(cls, direction_string, arrivals_body):
        arrivals = []
        for direction_list in arrivals_body:
            # When there are no arrivals, the API gives us an empty list instead
            # of a dictionary
            if isinstance(direction_list, dict) \
                    and [*direction_list][0] == direction_string:
                arrivals.append(direction_list[direction_string])
        if arrivals:
            return arrivals[0]
        return []

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
                                 headsign=arrival['destination'],
                                 agency_timezone=cls.TIMEZONE)
