import pytest

from gtfs_realtime_translators.factories import FeedMessage
from gtfs_realtime_translators.translators import NjtBusGtfsRealtimeTranslator
from gtfs_realtime_translators.bindings import intersection_pb2 as intersection_gtfs_realtime


@pytest.fixture
def njt_bus():
    with open('test/fixtures/njt_bus.xml') as f:
        raw = f.read()
    return raw


def test_njt_data(njt_bus):
    translator = NjtBusGtfsRealtimeTranslator()
    message = translator(njt_bus)

    entity = message.entity[0]
    trip_update = entity.trip_update
    stop_time_update = trip_update.stop_time_update[0]

    assert message.header.gtfs_realtime_version == FeedMessage.VERSION
    assert entity.id == '1'
    assert trip_update.trip.route_id == '10'
    assert trip_update.trip.trip_id == '630'

    assert stop_time_update.stop_id == '43249'
    assert stop_time_update.arrival.time == 1621435140
    assert stop_time_update.departure.time == 1621435140

    intersection_trip_update = trip_update.Extensions[
        intersection_gtfs_realtime.intersection_trip_update]
    assert intersection_trip_update.headsign == '10 JERSEY CITY JOURNAL SQUARE-Exact Fare'
    assert intersection_trip_update.agency_timezone == 'America/New_York'

    intersection_stop_time_update = stop_time_update.Extensions[
        intersection_gtfs_realtime.intersection_stop_time_update]
    assert intersection_stop_time_update.scheduled_arrival.time == 1621435020
    assert intersection_stop_time_update.scheduled_departure.time == 1621435020
    assert intersection_stop_time_update.stop_name == 'JOURNAL SQUARE TRANSPORTATION CENTER'
