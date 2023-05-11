import pytest

from gtfs_realtime_translators.translators import MbtaGtfsRealtimeTranslator
from gtfs_realtime_translators.bindings import intersection_pb2 as intersection_gtfs_realtime
from gtfs_realtime_translators.factories import FeedMessage


@pytest.fixture
def mbta_subway():
    with open('test/fixtures/mbta_subway.json') as f:
        raw = f.read()
    return raw


@pytest.fixture
def mbta_subway_missing_static():
    with open('test/fixtures/mbta_subway_missing_static.json') as f:
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
    assert entity.trip_update.trip.trip_id == '55458948-19:45-GovernmentCenterWonderlandSuspend'
    assert stop_time_update.stop_id == '70045'
    assert stop_time_update.arrival.time == 1683144315
    assert stop_time_update.departure.time == 1683144381

def test_mbta_bus_realtime_arrival_departure(mbta_bus):
    translator = MbtaGtfsRealtimeTranslator()
    message = translator(mbta_bus)

    entity = message.entity[0]
    trip_update = entity.trip_update
    stop_time_update = trip_update.stop_time_update[0]

    assert message.header.gtfs_realtime_version == FeedMessage.VERSION

    assert entity.id == '1'
    assert entity.trip_update.trip.route_id == '66'
    assert entity.trip_update.trip.trip_id == '55800441'
    assert stop_time_update.stop_id == '1357'
    assert stop_time_update.arrival.time == 1683145580
    assert stop_time_update.departure.time == 1683145580

def test_mbta_bus_realtime_no_arrival_departure(mbta_bus):
    translator = MbtaGtfsRealtimeTranslator()
    message = translator(mbta_bus)

    entity = message.entity[1]
    trip_update = entity.trip_update
    stop_time_update = trip_update.stop_time_update[0]

    assert message.header.gtfs_realtime_version == FeedMessage.VERSION

    assert entity.id == '2'
    assert entity.trip_update.trip.route_id == '66'
    assert entity.trip_update.trip.trip_id == '55800443'
    assert stop_time_update.stop_id == '1357'
    assert stop_time_update.arrival.time == 1683145945
    assert stop_time_update.departure.time == 1683145945

def test_mbta_bus_realtime_arrival_no_departure(mbta_bus):
    translator = MbtaGtfsRealtimeTranslator()
    message = translator(mbta_bus)

    entity = message.entity[2]
    trip_update = entity.trip_update
    stop_time_update = trip_update.stop_time_update[0]

    assert message.header.gtfs_realtime_version == FeedMessage.VERSION

    assert entity.id == '3'
    assert entity.trip_update.trip.route_id == '66'
    assert entity.trip_update.trip.trip_id == '55800446'
    assert stop_time_update.stop_id == '1357'
    assert stop_time_update.arrival.time == 1683146412
    assert stop_time_update.departure.time == 1683146412

def test_mbta_subway_realtime_include_static_data(mbta_subway):
    translator = MbtaGtfsRealtimeTranslator()
    message = translator(mbta_subway)

    entity = message.entity[0]
    trip_update = entity.trip_update
    stop_time_update = trip_update.stop_time_update[0]

    assert trip_update.Extensions[
        intersection_gtfs_realtime.intersection_trip_update].route_short_name == 'BL'
    assert trip_update.Extensions[
        intersection_gtfs_realtime.intersection_trip_update].route_long_name == 'Blue Line'
    assert trip_update.Extensions[
        intersection_gtfs_realtime.intersection_trip_update].route_color == '003DA5'
    assert trip_update.Extensions[
        intersection_gtfs_realtime.intersection_trip_update].route_text_color == 'FFFFFF'
    assert trip_update.Extensions[
        intersection_gtfs_realtime.intersection_trip_update].headsign == 'Bowdoin'
    assert stop_time_update.Extensions[
        intersection_gtfs_realtime.intersection_stop_time_update].stop_name == 'Maverick'
    assert stop_time_update.Extensions[
        intersection_gtfs_realtime.intersection_stop_time_update].scheduled_arrival.time == 1683297180
    assert stop_time_update.Extensions[
        intersection_gtfs_realtime.intersection_stop_time_update].scheduled_departure.time == 1683297180

def test_mbta_subway_realtime_missing_static_data(mbta_subway_missing_static):
    translator = MbtaGtfsRealtimeTranslator()
    message = translator(mbta_subway_missing_static)

    entity = message.entity[0]
    trip_update = entity.trip_update
    stop_time_update = trip_update.stop_time_update[0]

    assert trip_update.Extensions[
        intersection_gtfs_realtime.intersection_trip_update].route_short_name == 'BL'
    assert trip_update.Extensions[
        intersection_gtfs_realtime.intersection_trip_update].route_long_name == 'Blue Line'
    assert trip_update.Extensions[
        intersection_gtfs_realtime.intersection_trip_update].route_color == '003DA5'
    assert trip_update.Extensions[
        intersection_gtfs_realtime.intersection_trip_update].route_text_color == 'FFFFFF'
    assert trip_update.Extensions[
        intersection_gtfs_realtime.intersection_trip_update].headsign == 'Bowdoin'
    assert stop_time_update.Extensions[
        intersection_gtfs_realtime.intersection_stop_time_update].stop_name == ''
    assert stop_time_update.Extensions[
        intersection_gtfs_realtime.intersection_stop_time_update].scheduled_arrival.time == 0
    assert stop_time_update.Extensions[
        intersection_gtfs_realtime.intersection_stop_time_update].scheduled_departure.time == 0
