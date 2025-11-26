import json
import pendulum

from gtfs_realtime_translators.factories import FeedMessage, TripUpdate


class PathRailNewGtfsRealtimeTranslator:
    TIMEZONE = 'America/New_York'

    GREY_TRAIN_SERVICE_NUMBER = 0

    SERVICE_LOOKUP = {
        '5': {
            'JSQ': 'Journal Square Via Hoboken',
            '33S': '33rd St Via Hoboken',
            'HOB': 'Hoboken',
            'route_id': 'ATW'
        },
        '4': {
            'WTC': 'World Trade Center',
            'HOB': 'Hoboken',
            'route_id': 'GRE'
        },
        '3': {
            '33S': '33rd Street',
            'HOB': 'Hoboken',
            'route_id': 'BLU'
        },
        '2': {
            'JSQ': 'Journal Square',
            '33S': '33rd Street',
            'route_id': 'YEL'
        },
        '1': {
            'WTC': 'World Trade Center',
            'NWK': 'Newark',
            'route_id': 'RED'
        }
    }
    STOP_ID_LOOKUP = {
        'GRV': {
            "stop_name": 'Grove Street',
            "tracks": {
                "Tunnel H": '781726',
                "Tunnel G": '781727',
            }
        },
        'WTC': {
            "stop_name": 'World Trade Center',
            "tracks": {
                "Track 1": '7817471T1',
                "Track 2": '7817471T2',
                "Track 3": '7817471T3',
                "Track 4": '781750T4',
                "Track 5": '781750T5',
            }
        },
        'NWK': {
            "stop_name": 'Newark',
            "tracks": {
                "Track G": '781719',
                "Track H": '781718'
            }
        },
        'HAR': {
            "stop_name": 'Harrison',
            "tracks": {
                "Track H": '781720',
                "Track G": '781721',
            }
        },
        'EXP': {
            "stop_name": 'Exchange Place',
            "tracks": {
                "Tunnel E": '781731',
                "Tunnel F": '781730',
            }
        },
        "NEW": {
            "stop_name": 'Newport',
            "tracks": {
                "Tunnel E": '781728',
                "Tunnel F": '781729',
            }
        },
        "CHR": {
            "stop_name": 'Christopher Street',
            "tracks": {
                "Tunnel B": '781732',
                "Tunnel A": '781733'
            }
        },
        "09S": {
            "stop_name": '9th Street',
            "tracks": {
                "Tunnel B": '781734',
                "Tunnel A": '781735',
            }
        },
        "14S": {
            "stop_name": '14th Street',
            "tracks": {
                "Tunnel B": '781736',
                "Tunnel A": '781737',
            }

        },
        "23S": {
            "stop_name": '23rd Street',
            "tracks": {
                "Tunnel B": '781738',
                "Tunnel A": '781739',
            }
        },
        "JSQ": {
            "stop_name": 'Journal Square',
            "tracks": {
                "Track 1": '781722',
                "Track 2": '781723',
                "Track 3": '781724',
                "Track 4": '781725',
            }
        },
        "33S": {
            "stop_name": '33rd Street',
            "tracks": {
                "Track 1": '781742T1',
                "Track 2": '781740',
                "Track 3": '781742T3',
            }
        },
        "HOB": {
            "stop_name": 'Hoboken',
            "tracks": {
                "Track 1": '781743',
                "Track 2": '781744T2',
                "Track 3": '781744T3'
            }
        }
    }

    """
       Since PATH GTFS data have stops that are, in most cases, unique to a route, direction, service date, and/or 
       destination, a mapping is created to ensure we return the appropriate stop_id/headsign/route information for a stop and track arrival updates.

       Keys are based off the "serviceID" field while also using a second lookup to determine the stop_id based on the track for a particular station
    """

    def __call__(self, data):
        json_data = json.loads(data)
        entities = self.__make_trip_updates(json_data)
        return FeedMessage.create(entities=entities)

    @classmethod
    def __to_unix_time(cls, time):
        datetime = int(pendulum.from_format(
            time, 'HH:mm').in_tz(cls.TIMEZONE).timestamp())
        return datetime

    @classmethod
    def __route_lookup(cls, service_id, station_shortkey, track_id,
                       destination):
        service_mapping = cls.SERVICE_LOOKUP.get(str(service_id))
        station_mapping = cls.STOP_ID_LOOKUP.get(station_shortkey)
        route_id = service_mapping.get('route_id')
        headsign = service_mapping.get(destination)
        stop_id = station_mapping.get("tracks").get(track_id)
        stop_name = station_mapping.get("stop_name")
        return {
            'route_id': route_id,
            'stop_id': stop_id,
            'headsign': headsign,
            'stop_name': stop_name
        }

    @classmethod
    def __should_skip_update(cls, route_data):
        should_skip = False
        for key, value in route_data.items():
            if value is None:
                should_skip = True
                break
        return should_skip

    @classmethod
    def __is_grey_train(cls, service_id):
        return service_id == cls.GREY_TRAIN_SERVICE_NUMBER

    @classmethod
    def __make_trip_updates(cls, data):
        trip_updates = []
        stations = data['stations']
        for station in stations:
            station_shortkey = station['abbrv']
            tracks = station.get('tracks')
            if station_shortkey == 'systemwide':
                continue
            for track in tracks:
                track_id = track.get('trackId')
                trains = track.get('trains', {})
                for idx, train in enumerate(trains):
                    if not train.get('trainId'):
                        continue
                    train_info = train.get('trainId').split('_')
                    service_id = train.get('service')
                    if cls.__is_grey_train(service_id):
                        continue
                    destination = train.get('destination')
                    arrival_time = train.get('depArrTime')
                    scheduled_arrival_time = cls.__to_unix_time(train_info[0])
                    arrival_data = cls.__route_lookup(
                        service_id, station_shortkey, track_id, destination)
                    if cls.__should_skip_update(arrival_data):
                        continue
                    trip_update = TripUpdate.create(
                        entity_id=train.get('trainId').strip(),
                        departure_time=arrival_time,
                        arrival_time=arrival_time,
                        scheduled_arrival_time=scheduled_arrival_time,
                        scheduled_departure_time=scheduled_arrival_time,
                        track=track_id,
                        route_id=arrival_data.get(
                            'route_id'),
                        stop_id=arrival_data.get(
                            'stop_id'),
                        headsign=arrival_data.get(
                            'headsign'),
                        stop_name=arrival_data.get('stop_name'),
                        agency_timezone=cls.TIMEZONE)
                    trip_updates.append(trip_update)

        return trip_updates
