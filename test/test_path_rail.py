import pytest

from gtfs_realtime_translators.factories import FeedMessage
from gtfs_realtime_translators.translators.path_rail import PathGtfsRealtimeTranslator
from gtfs_realtime_translators.bindings import intersection_pb2 as intersection_gtfs_realtime


@pytest.fixture
def path_rail():
    with open('test/fixtures/path_rail.json') as f:
        raw = f.read()
    return raw


def test_path_data(path_rail):
    translator = PathGtfsRealtimeTranslator()
    message = translator(path_rail)

    assert message.header.gtfs_realtime_version == FeedMessage.VERSION

    entity = message.entity[0]
    trip_update = entity.trip_update
    assert trip_update.trip.trip_id == '88888'
    assert trip_update.trip.route_id == '99999'

    stop_time_update = trip_update.stop_time_update[0]
    assert stop_time_update.stop_id == 'a-stop-id'
    assert stop_time_update.departure.time == 1570045710
    assert stop_time_update.arrival.time == 1570045710

    intersection_trip_update = trip_update.Extensions[intersection_gtfs_realtime.intersection_trip_update]
    assert intersection_trip_update.custom_status == '3 min'
