from google.transit import gtfs_realtime_pb2 as gtfs_realtime

from gtfs_realtime_translators.bindings import intersection_pb2 as intersection_gtfs_realtime


class CtaGtfsRealtimeTranslator:
    """CTA signals a delayed vehicle via NO_DATA + no arrival.time, per Metra's convention."""

    def __call__(self, data):
        feed_message = gtfs_realtime.FeedMessage()
        feed_message.ParseFromString(data)

        for entity in feed_message.entity:
            if not entity.HasField('trip_update'):
                continue
            trip_update = entity.trip_update
            if self.__is_delayed(trip_update):
                trip_update.Extensions[intersection_gtfs_realtime.intersection_trip_update].custom_status = 'DELAYED'

        return feed_message

    @staticmethod
    def __is_delayed(trip_update):
        return any(
            stop_time_update.schedule_relationship == gtfs_realtime.TripUpdate.StopTimeUpdate.NO_DATA
            and not stop_time_update.arrival.HasField('time')
            for stop_time_update in trip_update.stop_time_update
        )
