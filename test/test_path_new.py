import pendulum
import pytest

from gtfs_realtime_translators.factories import FeedMessage
from gtfs_realtime_translators.translators.path_new import PathNewGtfsRealtimeTranslator
from gtfs_realtime_translators.bindings import intersection_pb2 as intersection_gtfs_realtime


@pytest.fixture
def path_new():
    with open('test/fixtures/path_new.json') as f:
        raw = f.read()
    return raw


def test_path_data(path_new):
    translator = PathNewGtfsRealtimeTranslator()
    with pendulum.travel_to(pendulum.datetime(2020, 2, 22, 12, 0, 0)):
        message = translator(path_new)
    assert message.header.gtfs_realtime_version == FeedMessage.VERSION
    entity = message.entity[0]
    assert entity.id == '15:55_NWK/WTC'
    trip_update = entity.trip_update
    assert trip_update.trip.trip_id == ''
    assert trip_update.trip.route_id == '862'
    stop_time_update = trip_update.stop_time_update[0]
    assert stop_time_update.stop_id == '781718'
    assert stop_time_update.departure.time == 1635796500
    assert stop_time_update.arrival.time == 1635796500
    intersection_trip_update = trip_update.Extensions[intersection_gtfs_realtime.intersection_trip_update]
    intersection_stop_time_update = stop_time_update.Extensions[intersection_gtfs_realtime.intersection_stop_time_update]
    assert intersection_stop_time_update.track == "Track H"
    assert intersection_stop_time_update.stop_name == "Newark"
    assert intersection_trip_update.headsign == "World Trade Center"
