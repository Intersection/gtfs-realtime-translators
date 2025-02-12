import pytest
import pendulum

from gtfs_realtime_translators.translators import CtaBusGtfsRealtimeTranslator
from gtfs_realtime_translators.bindings import intersection_pb2 as intersection_gtfs_realtime
from gtfs_realtime_translators.factories import FeedMessage


@pytest.fixture
def cta_bus():
    with open('test/fixtures/cta_bus.json') as f:
        raw = f.read()
    return raw


def test_cta_bus_realtime_arrival(cta_bus):
    translator = CtaBusGtfsRealtimeTranslator()
    with pendulum.travel_to(pendulum.datetime(2019, 2, 20, 17)):
        message = translator(cta_bus)

    entity = message.entity[0]
    trip_update = entity.trip_update
    stop_time_update = trip_update.stop_time_update[0]

    assert message.header.gtfs_realtime_version == FeedMessage.VERSION

    assert entity.id == '1'
    assert entity.trip_update.trip.route_id == '147'
    assert stop_time_update.stop_id == '1203'
    assert stop_time_update.arrival.time == 1570531080

    # Test Intersection extensions
    intersection_trip_update = trip_update.Extensions[intersection_gtfs_realtime.intersection_trip_update]
    assert intersection_trip_update.headsign == 'Howard Station'
    assert intersection_trip_update.custom_status == '3 min'

def test_cta_bus_scheduled_departure(cta_bus):
    translator = CtaBusGtfsRealtimeTranslator()
    with pendulum.travel_to(pendulum.datetime(2019, 2, 20, 17)):
        message = translator(cta_bus)

    entity = message.entity[1]
    trip_update = entity.trip_update
    stop_time_update = trip_update.stop_time_update[0]

    assert entity.id == '2'
    assert stop_time_update.arrival.time == 1570531500

    # Test Intersection extensions
    intersection_trip_update = trip_update.Extensions[intersection_gtfs_realtime.intersection_trip_update]
    assert intersection_trip_update.custom_status == '10 min'

