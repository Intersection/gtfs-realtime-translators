import pytest
import pendulum

from gtfs_realtime_translators.translators import SwiftlyGtfsRealtimeTranslator
from gtfs_realtime_translators.factories import FeedMessage
from gtfs_realtime_translators.bindings import intersection_pb2 as intersection_gtfs_realtime


@pytest.fixture
def septa_trolley_lines():
    with open('test/fixtures/septa_trolley_lines.json') as f:
        raw = f.read()

    return raw


def test_septa_trolley_data(septa_trolley_lines):
    translator = SwiftlyGtfsRealtimeTranslator(stop_id='20646')
    with pendulum.travel_to(pendulum.datetime(2021,6,16,12,0,0)):
        message = translator(septa_trolley_lines)

    # check first entity
    entity = message.entity[0]
    trip_update = entity.trip_update
    stop_time_update = trip_update.stop_time_update[0]

    assert message.header.gtfs_realtime_version == FeedMessage.VERSION

    assert len(message.entity) == 4

    assert entity.id == '1'

    assert trip_update.trip.trip_id == '609813'
    assert trip_update.trip.route_id == '11'

    assert stop_time_update.arrival.time == 1623846660
    assert stop_time_update.departure.time == 1623846660
    assert stop_time_update.stop_id == '20646'

    # test extensions
    ixn_stop_time_updates = stop_time_update.Extensions[intersection_gtfs_realtime.intersection_stop_time_update]
    ixn_trip_updates = trip_update.Extensions[intersection_gtfs_realtime.intersection_trip_update]
    assert ixn_stop_time_updates.stop_name == "19th St Trolley Station"
    assert ixn_trip_updates.headsign == "13th-Market"
    assert ixn_trip_updates.route_short_name == "11"
    assert ixn_trip_updates.route_long_name == "11 - 13th-Market to Darby Trans Cntr"

    # check last entity
    entity = message.entity[3]
    trip_update = entity.trip_update
    stop_time_update = trip_update.stop_time_update[0]

    assert entity.id == '3'

    assert trip_update.trip.trip_id == '610889'
    assert trip_update.trip.route_id == '13'

    assert stop_time_update.arrival.time == 1623847140
    assert stop_time_update.departure.time == 1623847140
    assert stop_time_update.stop_id == '20646'

    # test extensions
    ixn_stop_time_updates = stop_time_update.Extensions[intersection_gtfs_realtime.intersection_stop_time_update]
    ixn_trip_updates = trip_update.Extensions[intersection_gtfs_realtime.intersection_trip_update]
    assert ixn_stop_time_updates.stop_name == "19th St Trolley Station"
    assert ixn_trip_updates.headsign == "13th-Market"
    assert ixn_trip_updates.route_short_name == "13"
    assert ixn_trip_updates.route_long_name == "13 - 13th-Market to Yeadon-Darby"
