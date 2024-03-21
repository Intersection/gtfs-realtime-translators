import pytest
import pendulum

from gtfs_realtime_translators.translators import CtaSubwayGtfsRealtimeTranslator
from gtfs_realtime_translators.bindings import intersection_pb2 as intersection_gtfs_realtime
from gtfs_realtime_translators.factories import FeedMessage


@pytest.fixture
def cta_subway():
    with open('test/fixtures/cta_subway.json') as f:
        raw = f.read()

    return raw


def test_cta_subway_realtime_arrival(cta_subway):
    translator = CtaSubwayGtfsRealtimeTranslator()
    with pendulum.travel_to(pendulum.datetime(2019, 2, 20, 17)):
        message = translator(cta_subway)

    entity = message.entity[0]
    trip_update = entity.trip_update
    stop_time_update = trip_update.stop_time_update[0]

    assert message.header.gtfs_realtime_version == FeedMessage.VERSION

    assert entity.id == '1'
    assert entity.trip_update.trip.route_id == 'Red'
    assert stop_time_update.stop_id == '30251'
    assert stop_time_update.arrival.time == 1570458602

    # Test Intersection extensions
    intersection_trip_update = trip_update.Extensions[intersection_gtfs_realtime.intersection_trip_update]
    assert intersection_trip_update.headsign == 'Howard'

    intersection_stop_time_update = stop_time_update.Extensions[intersection_gtfs_realtime.intersection_stop_time_update]
    assert intersection_stop_time_update.scheduled_arrival.time == 0

def test_cta_subway_scheduled_arrival(cta_subway):
    translator = CtaSubwayGtfsRealtimeTranslator()
    with pendulum.travel_to(pendulum.datetime(2019, 2, 20, 17)):
        message = translator(cta_subway)

    entity = message.entity[1]
    trip_update = entity.trip_update
    stop_time_update = trip_update.stop_time_update[0]

    assert entity.id == '2'
    assert stop_time_update.arrival.time == 0

    # Test Intersection extensions
    intersection_stop_time_update = stop_time_update.Extensions[intersection_gtfs_realtime.intersection_stop_time_update]
    assert intersection_stop_time_update.scheduled_arrival.time == 1570458776
