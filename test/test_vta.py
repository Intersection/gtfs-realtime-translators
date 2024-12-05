import pytest
import pendulum

from gtfs_realtime_translators.translators import SwiftlyGtfsRealtimeTranslator
from gtfs_realtime_translators.factories import FeedMessage
from gtfs_realtime_translators.bindings import intersection_pb2 as intersection_gtfs_realtime


@pytest.fixture
def vta_rail():
    with open('test/fixtures/vta_rail.json') as f:
        raw = f.read()

    return raw


def test_vta_data(vta_rail):
    translator = SwiftlyGtfsRealtimeTranslator(stop_id='5236')
    with pendulum.travel_to(pendulum.datetime(2019,2,20,17,0,0)):
        message = translator(vta_rail)

    entity = message.entity[0]
    trip_update = entity.trip_update
    stop_time_update = trip_update.stop_time_update[0]

    assert message.header.gtfs_realtime_version == FeedMessage.VERSION

    assert entity.id == '1'

    assert trip_update.trip.trip_id == '2960461'
    assert trip_update.trip.route_id == 'Ornge'

    assert stop_time_update.arrival.time == 1550682060
    assert stop_time_update.departure.time == 1550682060
    assert stop_time_update.stop_id == '5236'

    # test extensions
    ixn_stop_time_updates = stop_time_update.Extensions[intersection_gtfs_realtime.intersection_stop_time_update]
    ixn_trip_updates = trip_update.Extensions[intersection_gtfs_realtime.intersection_trip_update]
    assert ixn_stop_time_updates.stop_name == "Milpitas Station"
    assert ixn_trip_updates.headsign == "Alum Rock"
    assert ixn_trip_updates.route_short_name == "Orange Line"
    assert ixn_trip_updates.route_long_name == "Orange Line - Mountain View - Alum Rock"
