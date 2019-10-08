from google.transit import gtfs_realtime_pb2 as gtfs_realtime

from gtfs_realtime_translators.bindings import intersection_pb2 as intersection_gtfs_realtime

class Entity:

    @staticmethod
    def create(entity_id, **kwargs):
        return gtfs_realtime.FeedEntity(id=entity_id, **kwargs)


class TripUpdate:

    @staticmethod
    def __get_stop_time_events(arrival_time, departure_time=None):
        arrival = gtfs_realtime.TripUpdate.StopTimeEvent(time=arrival_time)
        if departure_time is None:
            departure = arrival
        else:
            departure = gtfs_realtime.TripUpdate.StopTimeEvent(time=departure_time)

        return arrival, departure

    @staticmethod
    def create(*args, **kwargs):
        entity_id = kwargs['entity_id']
        arrival_time = kwargs['arrival_time']
        departure_time = kwargs.get('departure_time', None)
        trip_id = kwargs.get('trip_id', None)
        route_id = kwargs.get('route_id', None)
        stop_id = kwargs['stop_id']

        # Intersection Extensions
        headsign = kwargs.get('headsign', None)
        track = kwargs.get('track', None)
        scheduled_arrival = kwargs.get('scheduled_arrival_time', None)
        scheduled_departure = kwargs.get('scheduled_departure_time', None)
        stop_name = kwargs.get('stop_name', None)
        route_short_name = kwargs.get('route_short_name', None)
        route_long_name = kwargs.get('route_long_name', None)
        route_color = kwargs.get('route_color', None)
        route_text_color = kwargs.get('route_text_color', None)
        block_id = kwargs.get('block_id', None)
        agency_timezone = kwargs.get('agency_timezone', None)
        custom_status = kwargs.get('custom_status', None)

        trip_descriptor = gtfs_realtime.TripDescriptor(trip_id=trip_id,
                                                       route_id=route_id)
        arrival, departure = TripUpdate.__get_stop_time_events(arrival_time, departure_time)
        stop_time_update = gtfs_realtime.TripUpdate.StopTimeUpdate(arrival=arrival,
                                                                   departure=departure,
                                                                   stop_id=stop_id)

        if track:
            stop_time_update.Extensions[intersection_gtfs_realtime.intersection_stop_time_update].track = track
        if scheduled_arrival:
            stop_time_update.Extensions[intersection_gtfs_realtime.intersection_stop_time_update].scheduled_arrival.time = scheduled_arrival
        if scheduled_departure:
            stop_time_update.Extensions[intersection_gtfs_realtime.intersection_stop_time_update].scheduled_departure.time = scheduled_departure
        if stop_name:
            stop_time_update.Extensions[intersection_gtfs_realtime.intersection_stop_time_update].stop_name = stop_name

        trip_update = gtfs_realtime.TripUpdate(trip=trip_descriptor,
                                               stop_time_update=[stop_time_update])

        if headsign:
            trip_update.Extensions[intersection_gtfs_realtime.intersection_trip_update].headsign = headsign
        if route_short_name:
            trip_update.Extensions[intersection_gtfs_realtime.intersection_trip_update].route_short_name = route_short_name
        if route_long_name:
            trip_update.Extensions[intersection_gtfs_realtime.intersection_trip_update].route_long_name = route_long_name
        if route_color:
            trip_update.Extensions[intersection_gtfs_realtime.intersection_trip_update].route_color = route_color
        if route_text_color:
            trip_update.Extensions[intersection_gtfs_realtime.intersection_trip_update].route_text_color = route_text_color
        if block_id:
            trip_update.Extensions[intersection_gtfs_realtime.intersection_trip_update].block_id = block_id
        if agency_timezone:
            trip_update.Extensions[intersection_gtfs_realtime.intersection_trip_update].agency_timezone = agency_timezone
        if custom_status:
            trip_update.Extensions[intersection_gtfs_realtime.intersection_trip_update].custom_status = custom_status

        return Entity.create(entity_id,
                             trip_update=trip_update)


class FeedMessage:
    VERSION = '2.0'

    @staticmethod
    def create(*args, **kwargs):
        entities = kwargs['entities']
        header = gtfs_realtime.FeedHeader(gtfs_realtime_version=FeedMessage.VERSION)
        message = gtfs_realtime.FeedMessage(header=header,
                                            entity=entities)
        return message
