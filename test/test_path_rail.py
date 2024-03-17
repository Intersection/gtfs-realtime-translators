import pendulum
import pytest

from gtfs_realtime_translators.factories import FeedMessage
from gtfs_realtime_translators.translators.path_rail import PathGtfsRealtimeTranslator


@pytest.fixture
def path_rail():
    with open('test/fixtures/path_rail.json') as f:
        raw = f.read()
    return raw


def test_path_data(path_rail):
    translator = PathGtfsRealtimeTranslator()
    with pendulum.travel_to(pendulum.datetime(2020, 2, 22, 12, 0, 0)):
        message = translator(path_rail)

    assert message.header.gtfs_realtime_version == FeedMessage.VERSION

    entity = message.entity[0]
    trip_update = entity.trip_update
    assert trip_update.trip.trip_id == ''
    assert trip_update.trip.route_id == '861'

    stop_time_update = trip_update.stop_time_update[0]
    assert stop_time_update.stop_id == '781741'
    assert stop_time_update.departure.time == 1582372920
    assert stop_time_update.arrival.time == 1582372920