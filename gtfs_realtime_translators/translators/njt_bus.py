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
    def __make_trip_updates(cls, data, filtered_stops):
        trip_updates = []
        trips = data['SCHEDULEROWSET'].values()

        for value in trips:
            for idx, item_entry in enumerate(value):
                # Intersection Extensions
                headsign = item_entry['busheader']
                trip_id = item_entry['gtfs_trip_id']
                route_id = item_entry['route']
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

                        # Skip Stop if stop_id is not found
                        if stop_id is None:
                            continue

                        # Skip Stop if stop_id is not in filtered stops
                        if filtered_stops.index(stop_id) < 0 :
                            continue

                        stop_name = stop['stopname']
                        track = stop['manual_lane_gate']
                        if track is None:
                            track = stop['scheduled_lane_gate']

                        scheduleddeparturedate = stop['scheduleddeparturedate']
                        scheduleddeparturetime = stop['scheduleddeparturetime']
                        scheduled_datetime = cls.__to_unix_time("{} {}".format(scheduleddeparturedate.title(), scheduleddeparturetime))
                        scheduled_departure_time = int(scheduled_datetime.timestamp())

                        arrival_time = int(scheduled_datetime.add(seconds=int(stop['sec_late'])).timestamp())

                        trip_update = TripUpdate.create(entity_id=str(idx + 1),
                                                        route_id=route_id,
                                                        trip_id=trip_id,
                                                        stop_id=stop_id,
                                                        headsign=headsign,
                                                        stop_name = stop_name,
                                                        track = track,
                                                        arrival_time = arrival_time,
                                                        departure_time = arrival_time,
                                                        scheduled_departure_time = scheduled_departure_time,
                                                        scheduled_arrival_time = scheduled_departure_time,
                                                        agency_timezone=cls.TIMEZONE)
                        trip_updates.append(trip_update)

        return trip_updates


class NJTBusStopCodeIdMappings:

    stops = {
        '20883':'2916',
        '19001':'39787',
        '19161':'39142',
        '18582':'2183',
        '21708':'40398',
    }

    @classmethod
    def get_stop_id(cls, stop_code):
        try:
            return cls.stops[stop_code]
        except KeyError:
            return None
