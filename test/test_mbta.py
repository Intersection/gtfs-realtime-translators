import pytest
import pendulum

from gtfs_realtime_translators.translators import MbtaGtfsRealtimeTranslator
from gtfs_realtime_translators.bindings import intersection_pb2 as intersection_gtfs_realtime
from gtfs_realtime_translators.factories import FeedMessage


@pytest.fixture
def mbta_subway():
    with open('test/fixtures/mbta_subway.json') as f:
        raw = f.read()
    return raw

@pytest.fixture
def mbta_bus():
    with open('test/fixtures/mbta_bus.json') as f:
        raw = f.read()
    return raw

def test_mbta_subway_realtime_arrival(mbta_subway):
    translator = MbtaGtfsRealtimeTranslator()
    message = translator(mbta_subway)

    entity = message.entity[0]
    trip_update = entity.trip_update
    stop_time_update = trip_update.stop_time_update[0]

    assert message.header.gtfs_realtime_version == FeedMessage.VERSION

    assert entity.id == '1'
    assert entity.trip_update.trip.route_id == 'Blue'
    assert entity.trip_update.trip.trip_id == '49417961'
    assert stop_time_update.stop_id == '70045'
    assert stop_time_update.arrival.time == 1632770790
    assert stop_time_update.departure.time == 1632770846

def test_mbta_bus_realtime_arrival(mbta_bus):
    translator = MbtaGtfsRealtimeTranslator()
    message = translator(mbta_bus)

    entity = message.entity[0]
    trip_update = entity.trip_update
    stop_time_update = trip_update.stop_time_update[0]

    assert message.header.gtfs_realtime_version == FeedMessage.VERSION

    assert entity.id == '3'
    assert entity.trip_update.trip.route_id == '66'
    assert entity.trip_update.trip.trip_id == '49181349'
    assert stop_time_update.stop_id == '1357'
    assert stop_time_update.arrival.time == 1632778733
    assert stop_time_update.departure.time == 1632778733

