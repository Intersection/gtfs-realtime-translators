from google.transit import gtfs_realtime_pb2 as gtfs_realtime

from gtfs_realtime_translators.bindings import intersection_pb2 as intersection_gtfs_realtime
from gtfs_realtime_translators.translators import CtaGtfsRealtimeTranslator


def _make_feed(stop_time_updates):
    feed = gtfs_realtime.FeedMessage()
    feed.header.gtfs_realtime_version = '2.0'
    entity = feed.entity.add()
    entity.id = '1'
    entity.trip_update.trip.trip_id = 'trip1'
    for stop_id, schedule_relationship, arrival_time in stop_time_updates:
        stop_time_update = entity.trip_update.stop_time_update.add()
        stop_time_update.stop_id = stop_id
        stop_time_update.schedule_relationship = schedule_relationship
        if arrival_time is not None:
            stop_time_update.arrival.time = arrival_time
    return feed.SerializeToString()


def test_cta_realtime_marks_no_data_trip_as_delayed():
    data = _make_feed([
        ('stop1', gtfs_realtime.TripUpdate.StopTimeUpdate.NO_DATA, None),
    ])

    translator = CtaGtfsRealtimeTranslator()
    message = translator(data)

    trip_update = message.entity[0].trip_update
    custom_status = trip_update.Extensions[intersection_gtfs_realtime.intersection_trip_update].custom_status
    assert custom_status == 'DELAYED'


def test_cta_realtime_leaves_scheduled_trip_unmarked():
    data = _make_feed([
        ('stop1', gtfs_realtime.TripUpdate.StopTimeUpdate.SCHEDULED, 11111),
    ])

    translator = CtaGtfsRealtimeTranslator()
    message = translator(data)

    trip_update = message.entity[0].trip_update
    custom_status = trip_update.Extensions[intersection_gtfs_realtime.intersection_trip_update].custom_status
    assert custom_status == ''


def test_cta_realtime_no_data_with_arrival_time_is_not_delayed():
    data = _make_feed([
        ('stop1', gtfs_realtime.TripUpdate.StopTimeUpdate.NO_DATA, 11111),
    ])

    translator = CtaGtfsRealtimeTranslator()
    message = translator(data)

    trip_update = message.entity[0].trip_update
    custom_status = trip_update.Extensions[intersection_gtfs_realtime.intersection_trip_update].custom_status
    assert custom_status == ''
