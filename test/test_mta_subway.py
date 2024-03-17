import pytest
import pendulum

from gtfs_realtime_translators.translators import MtaSubwayGtfsRealtimeTranslator
from gtfs_realtime_translators.bindings import intersection_pb2 as intersection_gtfs_realtime
from gtfs_realtime_translators.factories import FeedMessage


@pytest.fixture
def mta_subway():
    with open('test/fixtures/mta_subway.json') as f:
        raw = f.read()

    return raw


def test_mta_subway_data(mta_subway):
    translator = MtaSubwayGtfsRealtimeTranslator()
    with pendulum.travel_to(pendulum.datetime(2019,2,20,17,0,0)):
        message = translator(mta_subway)

    entity = message.entity[0]
    trip_update = entity.trip_update
    stop_time_update = trip_update.stop_time_update[0]

    assert message.header.gtfs_realtime_version == FeedMessage.VERSION

    assert entity.id == '1'

    assert stop_time_update.arrival.time == 1569507335
    assert stop_time_update.departure.time == 1569507335
    assert stop_time_update.stop_id == '101N'
    assert entity.trip_update.trip.route_id == '1'
    assert entity.trip_update.trip.trip_id == '2351'

    assert stop_time_update.Extensions[intersection_gtfs_realtime.intersection_stop_time_update].stop_name == 'Van Cortlandt Park - 242 St'
