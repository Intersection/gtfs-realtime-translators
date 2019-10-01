import pendulum
import pytest

from gtfs_realtime_translators.factories import FeedMessage
from gtfs_realtime_translators.translators import NjtRailTranslator


@pytest.fixture
def njt_rail():
    with open('test/fixtures/njt_rail_departure_vision.xml') as f:
        raw = f.read()
    return raw


def test_njt_data(njt_rail):
    with pendulum.test(pendulum.datetime(2019, 10, 1, 1, 0, 0, tz='America/New_York')):
        translator = NjtRailTranslator(njt_rail, station_id='NP') #  https://usermanual.wiki/Document/NJTRANSIT20REAL20Time20Data20Interface20Instructions2020Ver2025.785373145.pdf
    message = translator.feed_message

    # test that trip update is created with
    # entity_id, departure_time, stop_id as station_id, route_id, scheduled_departure_time, track, headsign

    entity = message.entity[0]
    trip_update = entity.trip_update
    stop_time_update = trip_update.stop_time_update[0]

    assert message.header.gtfs_realtime_version == FeedMessage.VERSION
    assert entity.id == '1'

    assert trip_update.trip.trip_id is None

    assert stop_time_update.stop_id == 'NP' # station_id from above
    assert stop_time_update.departure_time == 123456789
    assert stop_time_update.scheduled_departure_time == 123456789

    feed_bytes == translator.serialize()
    assert type(feed_bytes) == bytes
