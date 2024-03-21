import pytest

from gtfs_realtime_translators.factories import FeedMessage
from gtfs_realtime_translators.translators import NjtRailGtfsRealtimeTranslator
from gtfs_realtime_translators.bindings import intersection_pb2 as intersection_gtfs_realtime


@pytest.fixture
def njt_rail():
    with open('test/fixtures/njt_rail.xml') as f:
        raw = f.read()
    return raw


def test_njt_data(njt_rail):
    translator = NjtRailGtfsRealtimeTranslator()
    message = translator(njt_rail)

    entity = message.entity[6]
    trip_update = entity.trip_update
    stop_time_update = trip_update.stop_time_update[0]

    assert message.header.gtfs_realtime_version == FeedMessage.VERSION
    assert entity.id == '7'

    assert trip_update.trip.trip_id == ''
    assert trip_update.trip.route_id == '10'

    assert stop_time_update.stop_id == 'NP'
    assert stop_time_update.departure.time == 1570045710
    assert stop_time_update.arrival.time == 1570045710

    intersection_trip_update = trip_update.Extensions[intersection_gtfs_realtime.intersection_trip_update]
    assert intersection_trip_update.headsign == 'New York'
    assert intersection_trip_update.route_short_name == 'NEC'
    assert intersection_trip_update.route_long_name == 'Northeast Corridor Line'
    assert intersection_trip_update.route_color == 'black'
    assert intersection_trip_update.route_text_color == 'white'
    assert intersection_trip_update.block_id == '3154'
    assert intersection_trip_update.agency_timezone == 'America/New_York'
    assert intersection_trip_update.custom_status == ''

    intersection_stop_time_update = stop_time_update.Extensions[intersection_gtfs_realtime.intersection_stop_time_update]
    assert intersection_stop_time_update.track == '1'
    assert intersection_stop_time_update.scheduled_arrival.time == 1570045710
    assert intersection_stop_time_update.scheduled_departure.time == 1570045710
    assert intersection_stop_time_update.stop_name == 'Newark Penn'


def test_njt_data_amtrak(njt_rail):
    translator = NjtRailGtfsRealtimeTranslator()
    message = translator(njt_rail)

    entity = message.entity[0]
    trip_update = entity.trip_update
    stop_time_update = trip_update.stop_time_update[0]

    assert message.header.gtfs_realtime_version == FeedMessage.VERSION
    assert entity.id == '1'

    assert trip_update.trip.trip_id == ''
    assert trip_update.trip.route_id == 'AMTK'

    assert stop_time_update.stop_id == 'NP'
    assert stop_time_update.departure.time == 1570044525
    assert stop_time_update.arrival.time == 1570044525

    intersection_trip_update = trip_update.Extensions[intersection_gtfs_realtime.intersection_trip_update]
    assert intersection_trip_update.headsign == 'Boston'
    assert intersection_trip_update.route_short_name == 'AMTRAK'
    assert intersection_trip_update.route_long_name == 'Amtrak'
    assert intersection_trip_update.route_color == '#FFFF00'
    assert intersection_trip_update.route_text_color == '#000000'
    assert intersection_trip_update.block_id == 'A176'
    assert intersection_trip_update.agency_timezone == 'America/New_York'
    assert intersection_trip_update.custom_status == 'All Aboard'

    intersection_stop_time_update = stop_time_update.Extensions[intersection_gtfs_realtime.intersection_stop_time_update]
    assert intersection_stop_time_update.track == '2'
    assert intersection_stop_time_update.scheduled_arrival.time == 1570042920
    assert intersection_stop_time_update.scheduled_departure.time == 1570042920

    entity = message.entity[15]
    trip_update = entity.trip_update
    stop_time_update = trip_update.stop_time_update[0]

    assert message.header.gtfs_realtime_version == FeedMessage.VERSION
    assert entity.id == '16'

    assert trip_update.trip.trip_id == ''
    assert trip_update.trip.route_id == 'AMTK'

    assert stop_time_update.stop_id == 'NP'
    assert stop_time_update.departure.time == 1570047420
    assert stop_time_update.arrival.time == 1570047420

    intersection_trip_update = trip_update.Extensions[intersection_gtfs_realtime.intersection_trip_update]
    assert intersection_trip_update.headsign == 'Washington'
    assert intersection_trip_update.route_short_name == 'ACELA EXPRESS'
    assert intersection_trip_update.route_long_name == 'Amtrak Acela Express'
    assert intersection_trip_update.route_color == '#FFFF00'
    assert intersection_trip_update.route_text_color == '#000000'
    assert intersection_trip_update.block_id == 'A2165'
    assert intersection_trip_update.agency_timezone == 'America/New_York'
    assert intersection_trip_update.custom_status == ''

    intersection_stop_time_update = stop_time_update.Extensions[intersection_gtfs_realtime.intersection_stop_time_update]
    assert intersection_stop_time_update.track == '3'
    assert intersection_stop_time_update.scheduled_arrival.time == 1570047420
    assert intersection_stop_time_update.scheduled_departure.time == 1570047420
