import pendulum

from gtfs_realtime_translators.factories import FeedMessage, TripUpdate
import xmltodict


class NjtRailGtfsRealtimeTranslator:

    def __init__(self, data, station_id=None):
        station_data = xmltodict.parse(data)

        entities = self.__make_trip_updates(station_id, station_data)
        self.feed_message = FeedMessage.create(entities=entities)

    @classmethod
    def __to_unix_time(cls, time):
        datetime = pendulum.from_format(time, 'DD-MMM-YYYY HH:mm:ss A', tz='America/New_York')
        datetime.in_tz('UTC')
        return datetime

    @classmethod
    def __make_trip_updates(cls, station_id, data):
        trip_updates = []

        station_data_item = data['STATION']['ITEMS'].values()
        for value in station_data_item:
            for idx, item_entry in enumerate(value):
                scheduled_datetime = cls.__to_unix_time(item_entry['SCHED_DEP_DATE'])
                scheduled_departure_time = int(scheduled_datetime.timestamp())
                departure_time = int(scheduled_datetime.add(seconds=int(item_entry['SEC_LATE'])).timestamp())
                route_id = None
                headsign = item_entry['DESTINATION']
                track = item_entry['TRACK']

                for stop in item_entry['STOPS'].values():
                    origin_and_destination = [stop[i] for i in (0, -1)]
                    route_id = cls.__get_route_id(line=item_entry['LINE'],
                                                  line_abbreviation=item_entry['LINEABBREVIATION'],
                                                  origin=origin_and_destination[0],
                                                  destination=origin_and_destination[1])

                print('---------------------------')
                trip_update = TripUpdate.create(entity_id=str(idx + 1),
                                                departure_time=departure_time,
                                                scheduled_departure_time=scheduled_departure_time,
                                                arrival_time=departure_time,
                                                scheduled_arrival_time=scheduled_departure_time,
                                                route_id=route_id,
                                                stop_id=station_id,
                                                headsign=headsign,
                                                track=track)
                print(trip_update)
                trip_updates.append(trip_update)

        return trip_updates

    @classmethod
    def __get_route_id(cls, **metadata):
        route_id_lookup = {
            'atlantic_city_ine': '1',
            'montclair-boonton_line': None,
            'main_line': '5',
            'bergen_county_line': '6',
            'morristown_line': '7',
            'gladstone_branch': '8',
            'northeast_corridor_line': '9',
            'north_jersey_coast_line': None,
        }

        key = 'amtrak' if metadata['line_abbreviation'] == 'AMTK' else metadata['line'].replace(' ', '_').lower()
        route_id = route_id_lookup.get(key, None)
        if route_id is not None:
            return route_id

        def get_route_id_by_origin_or_destination(line_key, line_name, origin, destination):
            origin_name = origin['NAME'].replace(' ', '_').lower()
            destination_name = destination['NAME'].replace(' ', '_').lower()
            if line_key == 'montclair-boonton_line':
                hoboken = 'hoboken'
                origins_and_destinations = {'denville', 'dover', 'mount_olive', 'lake_hopatcong', 'hackettstown'}
                if origin_name == hoboken and destination_name in origins_and_destinations:
                    return '2'
                if origin_name in origins_and_destinations and destination_name == hoboken:
                    return '2'
                return '3'

            if line_key == 'north_jersey_coast_line':
                origins_and_destinations = {'new_york_penn_station'}
                if origin_name in origins_and_destinations or destination_name in origins_and_destinations:
                    return '10'
                return '11'
            if line_key == 'amtrak':
                word = f'Amtrak {line_name}'.title()
                return word
            return None

        return get_route_id_by_origin_or_destination(key, metadata['line'], metadata['origin'], metadata['destination'])

    def serialize(self):
        return self.feed_message.SerializeToString()
