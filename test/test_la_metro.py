import pytest
import pendulum

from gtfs_realtime_translators.translators import LaMetroGtfsRealtimeTranslator
from gtfs_realtime_translators.factories import FeedMessage


@pytest.fixture
def la_metro_rail():
    with open('test/fixtures/la_metro_rail.json') as f:
        raw = f.read()

    return raw


def test_la_data(la_metro_rail):
    translator = LaMetroGtfsRealtimeTranslator(stop_id='80122')
    with pendulum.travel_to(pendulum.datetime(2019,2,20,17,0,0)):
        message = translator(la_metro_rail)

    entity = message.entity[0]
    trip_update = entity.trip_update
    stop_time_update = trip_update.stop_time_update[0]

    assert message.header.gtfs_realtime_version == FeedMessage.VERSION

    assert entity.id == '1'

    assert trip_update.trip.trip_id == '1234'
    assert trip_update.trip.route_id == '801'

    assert stop_time_update.arrival.time == 1550682480
    assert stop_time_update.departure.time == 1550682480
    assert stop_time_update.stop_id == '80122'


def test_la_data_with_floats(la_metro_rail):
    translator = LaMetroGtfsRealtimeTranslator(stop_id='80122')
    with pendulum.travel_to(pendulum.datetime(2019,2,20,17,0,0)):
        message = translator(la_metro_rail)

    entity = message.entity[1]
    trip_update = entity.trip_update
    stop_time_update = trip_update.stop_time_update[0]

    assert message.header.gtfs_realtime_version == FeedMessage.VERSION

    assert entity.id == '2'

    assert trip_update.trip.trip_id == '1235'
    assert trip_update.trip.route_id == '801'

    assert stop_time_update.arrival.time == 1550683200
    assert stop_time_update.departure.time == 1550683200
    assert stop_time_update.stop_id == '80122'


def test_la_trip_id_parsing():
    assert LaMetroGtfsRealtimeTranslator.calculate_trip_id('48109430_20190404') == '48109430'
    assert LaMetroGtfsRealtimeTranslator.calculate_trip_id('48109430_Mo') == '48109430'
    assert LaMetroGtfsRealtimeTranslator.calculate_trip_id('48109430') == '48109430'
    assert LaMetroGtfsRealtimeTranslator.calculate_trip_id('') == ''
    assert LaMetroGtfsRealtimeTranslator.calculate_trip_id(1) == 1
