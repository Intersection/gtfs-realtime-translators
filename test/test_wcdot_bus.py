import pytest

from gtfs_realtime_translators.translators import WcdotGtfsRealTimeTranslator
from gtfs_realtime_translators.factories import FeedMessage
from gtfs_realtime_translators.bindings import intersection_pb2 as intersection_gtfs_realtime

@pytest.fixture
def wcdot_bus():
    with open('test/fixtures/wcdot_bus.json') as f:
        raw = f.read()

    return raw

def test_wcdot_data(wcdot_bus):
    translator = WcdotGtfsRealTimeTranslator(stop_id='5142')
    message = translator(wcdot_bus)
    entity = message.entity[0]
    trip_update = entity.trip_update
    stop_time_update = trip_update.stop_time_update[0]
    assert trip_update.trip.trip_id == '8612'
    assert stop_time_update.arrival.delay == -60
    assert stop_time_update.departure.delay == -60
    assert trip_update.trip.route_id == "66"
    assert entity.id == "130"
    assert stop_time_update.stop_id == "5142"

def test_invalid_stop_id(wcdot_bus):
    translator = WcdotGtfsRealTimeTranslator(stop_id='99999')
    message = translator(wcdot_bus)
    entity = message.entity
    assert len(entity) == 0