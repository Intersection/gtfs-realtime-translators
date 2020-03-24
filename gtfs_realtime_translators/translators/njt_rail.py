import pendulum

from gtfs_realtime_translators.factories import FeedMessage, TripUpdate
import xmltodict


class NjtRailGtfsRealtimeTranslator:
    """
    This translator accepts data from NJT's proprietary Train Control system. It produces
    trip updates similar to GTFS realtime format but with some additional context in the absence of some
    required and conditionally required GTFS-RT fields.

    The motivation to produce this format is due to the following:
        1) The APIs do not provide a trip_id
        2) The documentation notes that their realtime data may not always accurately map to their GTFS data

    :param data: XML formatted realtime feed

    https://usermanual.wiki/Document/NJTRANSIT20REAL20Time20Data20Interface20Instructions2020Ver2025.785373145.pdf
    """

    TIMEZONE = 'America/New_York'

    def __call__(self, data):
        station_data = xmltodict.parse(data)
        entities = self.__make_trip_updates(station_data)
        return FeedMessage.create(entities=entities)

    @classmethod
    def __to_unix_time(cls, time):
        datetime = pendulum.from_format(time, 'DD-MMM-YYYY HH:mm:ss A', tz=cls.TIMEZONE).in_tz('UTC')
        return datetime

    @classmethod
    def __make_trip_updates(cls, data):
        trip_updates = []

        station_data_item = data['STATION']['ITEMS'].values()
        for value in station_data_item:
            for idx, item_entry in enumerate(value):

                # Intersection Extensions
                headsign = item_entry['DESTINATION']
                route_short_name = cls.__get_route_short_name(item_entry)
                route_long_name = cls.__get_route_long_name(item_entry)
                route_color = item_entry['BACKCOLOR']
                route_text_color = item_entry['FORECOLOR']
                block_id = item_entry['TRAIN_ID']
                track = item_entry['TRACK']
                stop_id = data['STATION']['STATION_2CHAR']
                stop_name = data['STATION']['STATIONNAME']
                scheduled_datetime = cls.__to_unix_time(item_entry['SCHED_DEP_DATE'])
                departure_time = int(scheduled_datetime.add(seconds=int(item_entry['SEC_LATE'])).timestamp())
                scheduled_departure_time = int(scheduled_datetime.timestamp())
                custom_status = item_entry['STATUS']

                origin_and_destination = None
                for stop in item_entry['STOPS'].values():
                    origin_and_destination = [stop[i] for i in (0, -1)]

                route_id = cls.__get_route_id(item_entry, origin_and_destination)

                trip_update = TripUpdate.create(entity_id=str(idx + 1),
                                                departure_time=departure_time,
                                                scheduled_departure_time=scheduled_departure_time,
                                                arrival_time=departure_time,
                                                scheduled_arrival_time=scheduled_departure_time,
                                                route_id=route_id,
                                                route_short_name=route_short_name,
                                                route_long_name=route_long_name,
                                                route_color=route_color,
                                                route_text_color=route_text_color,
                                                stop_id=stop_id,
                                                stop_name=stop_name,
                                                headsign=headsign,
                                                track=track,
                                                block_id=block_id,
                                                agency_timezone=cls.TIMEZONE,
                                                custom_status=custom_status)
                trip_updates.append(trip_update)

        return trip_updates

    @classmethod
    def __get_route_id(cls, data, origin_and_destination):
        """
        This function resolves route_ids for NJT.

        The algorithm is as follows:
        1) Try to get the route_id based on the line name (or line abbreviation for Amtrak), otherwise...
        2) Try to get the route_id based on the origin and destination, otherwise return None

        For #2, this logic is necessary to discern multiple routes that are mapped to the same line. For instance, the
        North Jersey Coast Line operates two different routes. All trains with an origin or destination
        of New York Penn Station should resolve to route_id 10 and the others route_id 11

        :param data: keyword args containing data needed to perform the route logic
        :param origin_and_destination: an array containing the origin at index 0 and destination at index 1
        :return: route_id
        """

        route_id = cls.__get_route_id_by_line_data(data)
        if route_id:
            return route_id
        if origin_and_destination:
            return cls.__get_route_id_by_origin_or_destination(data, origin_and_destination)
        return None

    @classmethod
    def __get_route_id_by_origin_or_destination(cls, data, origin_and_destination):
        origin = origin_and_destination[0]
        destination = origin_and_destination[1]
        origin_name = origin['NAME'].replace(' ', '_').lower()
        destination_name = destination['NAME'].replace(' ', '_').lower()

        key = data['LINE'].replace(' ', '_').lower()
        if key == 'montclair-boonton_line':
            hoboken = 'hoboken'
            origins_and_destinations = {'denville', 'dover', 'mount_olive', 'lake_hopatcong', 'hackettstown'}
            if origin_name == hoboken and destination_name in origins_and_destinations:
                return '2'
            if origin_name in origins_and_destinations and destination_name == hoboken:
                return '2'
            return '3'

        if key == 'north_jersey_coast_line':
            origins_and_destinations = {'new_york_penn_station'}
            if origin_name in origins_and_destinations or destination_name in origins_and_destinations:
                return '10'
            return '11'
        return None

    @classmethod
    def __get_route_id_by_line_data(cls, data):
        route_id_lookup = {
            'atlantic_city_line': '1',
            'main_line': '5',
            'bergen_county_line': '6',
            'morristown_line': '7',
            'morris_&_essex_line': '7',
            'gladstone_branch': '8',
            'northeast_corridor_line': '9',
            'pascack_valley_line': '13',
            'princeton_shuttle': '14',
            'raritan_valley_line': '15',
            'meadowlands_rail_line': '17',
        }

        amtrak_route_id = 'AMTK'
        if data['LINEABBREVIATION'] == amtrak_route_id:
            return amtrak_route_id

        key = data['LINE'].replace(' ', '_').lower()
        route_id = route_id_lookup.get(key, None)
        return route_id if route_id else None

    @classmethod
    def __get_route_long_name(cls, data):
        amtrak_prefix = 'AMTRAK'
        abbreviation = data['LINEABBREVIATION']
        if abbreviation == 'AMTK':
            return amtrak_prefix.title() if data['LINE'] == amtrak_prefix else f"Amtrak {data['LINE']}".title()
        return data['LINE']

    @classmethod
    def __get_route_short_name(cls, data):
        if data['LINEABBREVIATION'] == 'AMTK':
            return data['LINE']
        return data['LINEABBREVIATION']
