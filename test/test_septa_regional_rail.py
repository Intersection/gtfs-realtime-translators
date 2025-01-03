import pytest
import pendulum

from gtfs_realtime_translators.translators import SeptaRegionalRailTranslator
from gtfs_realtime_translators.factories import FeedMessage
from gtfs_realtime_translators.bindings import intersection_pb2 as intersection_gtfs_realtime


@pytest.fixture
def septa_regional_rail():
    with open('test/fixtures/septa_regional_rail.json') as f:
        raw = f.read()

    return raw


def test_septa_regional_rail(septa_regional_rail):
    with pendulum.travel_to(pendulum.datetime(2019,4,26,15,0,0, tz='America/New_York')):
        translator = SeptaRegionalRailTranslator(stop_id='90004', filter_seconds=7200)
        message = translator(septa_regional_rail)

    assert len(message.entity) == 57

    entity = message.entity[0]
    trip_update = entity.trip_update
    stop_time_update = trip_update.stop_time_update[0]

    assert message.header.gtfs_realtime_version == FeedMessage.VERSION

    assert entity.id == '1'

    assert trip_update.trip.route_id == 'FOX'
    assert trip_update.Extensions[intersection_gtfs_realtime.intersection_trip_update].headsign == 'Fox Chase'

    assert stop_time_update.arrival.time == 1556305921
    assert stop_time_update.departure.time == 1556305981
    assert stop_time_update.stop_id == '90004'
    assert stop_time_update.Extensions[intersection_gtfs_realtime.intersection_stop_time_update].track == '2'


def test_septa_regional_rail_with_delay(septa_regional_rail):
    with pendulum.travel_to(pendulum.datetime(2019,4,26,15,0,0, tz='America/New_York')):
        translator = SeptaRegionalRailTranslator(stop_id='90004', filter_seconds=7200)
        message = translator(septa_regional_rail)

    entity = message.entity[2]
    trip_update = entity.trip_update
    stop_time_update = trip_update.stop_time_update[0]

    assert message.header.gtfs_realtime_version == FeedMessage.VERSION

    assert entity.id == '3'

    assert trip_update.trip.route_id == 'MED'
    assert trip_update.Extensions[intersection_gtfs_realtime.intersection_trip_update].headsign == 'Warminster'

    assert stop_time_update.arrival.time == 1556306641
    assert stop_time_update.departure.time == 1556306700
    assert stop_time_update.stop_id == '90004'
    assert stop_time_update.Extensions[intersection_gtfs_realtime.intersection_stop_time_update].scheduled_arrival.time == 1556306581
    assert stop_time_update.Extensions[intersection_gtfs_realtime.intersection_stop_time_update].scheduled_departure.time == 1556306640
    assert stop_time_update.Extensions[intersection_gtfs_realtime.intersection_stop_time_update].track == '5'


def test_transform_arrival():
    arrival = {
        "direction": "N",
        "path": "R8N",
        "train_id": "838",
        "origin": "30th Street Station",
        "destination": "Fox Chase",
        "line": "Fox Chase",
        "status": "On Time",
        "service_type": "LOCAL",
        "next_station": "30th St",
        "sched_time": "2019-04-26 15:12:01.000",
        "depart_time": "2019-04-26 15:13:01.000",
        "track": "2",
        "track_change": None,
        "platform": "",
        "platform_change": None
    }

    transformed = SeptaRegionalRailTranslator.transform_arrival(arrival)

    assert arrival.keys() == transformed.keys()

    assert transformed['sched_time'] == 1556305921
    assert transformed['depart_time'] == 1556305981
    assert type(transformed['sched_time']) == int
    assert type(transformed['depart_time']) == int


def test_calculate_realtime():
    assert SeptaRegionalRailTranslator.calculate_realtime(1556305921, '1 min') == 1556305981
    assert SeptaRegionalRailTranslator.calculate_realtime(1556305921, '12 min') == 1556306641
    assert SeptaRegionalRailTranslator.calculate_realtime(1556305921, 'On Time') == 1556305921


def test_time_at():
    with pendulum.travel_to(pendulum.datetime(2019,3,8,12,0,0)):
        assert SeptaRegionalRailTranslator.calculate_time_at(seconds=1) == int(pendulum.datetime(2019,3,8,12,0,1).timestamp())
