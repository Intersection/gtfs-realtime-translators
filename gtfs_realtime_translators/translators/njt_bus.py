import pendulum
import xmltodict
from gtfs_realtime_translators.factories import FeedMessage, TripUpdate


class NjtBusGtfsRealtimeTranslator:

    TIMEZONE = 'America/New_York'

    def __init__(self, stop_list):
        self.filtered_stops = stop_list.split(',')
        if self.filtered_stops is None:
            raise ValueError('filtered_stops is required.')

    def __call__(self, data):
        station_data = xmltodict.parse(data)
        entities = self.__make_trip_updates(station_data, self.filtered_stops)
        return FeedMessage.create(entities=entities)

    @classmethod
    def __to_unix_time(cls, time):
        dt = pendulum.from_format(time, 'DD-MMM-YY HH:mm A', tz=cls.TIMEZONE).in_tz('UTC')
        return dt

    @classmethod
    def __skip_processing(cls, stop_id, filtered_stops):
        # Skip Stop if stop_id is not found
        if stop_id is None:
            return True
        # Skip Stop if stop_id is not in filtered stops
        if stop_id not in filtered_stops:
            return True
        return False

    @classmethod
    def __make_trip_updates(cls, data, filtered_stops):
        trip_updates = []
        trips = data['SCHEDULEROWSET'].values()

        for value in trips:
            for idx, item_entry in enumerate(value):
                # Intersection Extensions
                headsign = item_entry['busheader']
                trip_id = item_entry['gtfs_trip_id']
                route_id = item_entry['gtfs_route_id']
                if item_entry.get('STOP', None) is not None:
                    stops = item_entry['STOP']

                    # If there is only one <STOP> for the <TRIP> we have to explicitly create a list
                    if not isinstance(stops, list):
                       stops = [stops]

                    # Process Stops
                    for stop in stops:
                        stop_code = stop['gtfs_stop_Code']
                        # Get Stop ID for the given Stop Code From the Mapping
                        stop_id = NJTBusStopCodeIdMappings.get_stop_id(stop_code)

                        if cls.__skip_processing(stop_id, filtered_stops):
                            continue

                        stop_name = stop['stopname']
                        track = stop['manual_lane_gate']
                        if not track:
                            track = stop['scheduled_lane_gate']

                        scheduleddeparturedate = stop['scheduleddeparturedate']
                        scheduleddeparturetime = stop['scheduleddeparturetime']
                        scheduled_datetime = cls.__to_unix_time("{} {}".format(scheduleddeparturedate.title(), scheduleddeparturetime))
                        scheduled_departure_time = int(scheduled_datetime.timestamp())

                        sec_late = 0
                        if stop['sec_late']:
                            sec_late = int(stop['sec_late'])
                        arrival_time = int(scheduled_datetime.add(seconds=sec_late).timestamp())

                        trip_update = TripUpdate.create(entity_id=str(idx + 1),
                                                        route_id=route_id,
                                                        trip_id=trip_id,
                                                        stop_id=stop_id,
                                                        headsign=headsign,
                                                        stop_name=stop_name,
                                                        track=track,
                                                        arrival_time=arrival_time,
                                                        departure_time=arrival_time,
                                                        scheduled_departure_time=scheduled_departure_time,
                                                        scheduled_arrival_time=scheduled_departure_time,
                                                        agency_timezone=cls.TIMEZONE)
                        trip_updates.append(trip_update)

        return trip_updates


class NJTBusStopCodeIdMappings:

    stops = {
        '18741':'39786',
        '31890':'43283',
        '18733':'2240',
        '20486':'21066',
        '20481':'21128',
        '20883':'2916',
        '31731':'43248',
        '31732':'43249',
        '20647':'25584',
        '20643':'2859',
        '20497':'26641',
        '20496':'17082',
        '21129':'2866',
        '21134':'2867',
        '20913':'2873',
        '24570':'22594',
        '24434':'22805',
        '24982':'22599',
        '43469':'31997',
        '13697':'22647',
        '24090':'22733',
        '42132':'22585',
        '25104':'22736',
        '25179':'22649'
    }

    @classmethod
    def get_stop_id(cls, stop_code):
        try:
            return cls.stops[stop_code]
        except KeyError:
            return None
