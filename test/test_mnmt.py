import pytest

from gtfs_realtime_translators.translators import MnmtGtfsRealtimeTranslator
from gtfs_realtime_translators.bindings import intersection_pb2 as intersection_gtfs_realtime
from gtfs_realtime_translators.factories import FeedMessage


@pytest.fixture
def mnmt():
    with open('test/fixtures/mnmt.json') as f:
        raw = f.read()
    return raw


def test_mnmt_realtime_departure(mnmt):
    translator = MnmtGtfsRealtimeTranslator()
    message = translator(mnmt)

    entity = message.entity[0]
    trip_update = entity.trip_update
    stop_time_update = trip_update.stop_time_update[0]

    assert message.header.gtfs_realtime_version == FeedMessage.VERSION
    assert entity.id == '1'

    assert stop_time_update.departure.time == 1702923655
    assert stop_time_update.arrival.time == 1702923655

    assert not stop_time_update.Extensions[
               intersection_gtfs_realtime.intersection_stop_time_update].\
        scheduled_arrival.time
    assert not stop_time_update.Extensions[
               intersection_gtfs_realtime.intersection_stop_time_update].\
        scheduled_departure.time


def test_mnmt_scheduled_departure(mnmt):
    translator = MnmtGtfsRealtimeTranslator()
    message = translator(mnmt)

    entity = message.entity[1]
    trip_update = entity.trip_update
    stop_time_update = trip_update.stop_time_update[0]

    assert message.header.gtfs_realtime_version == FeedMessage.VERSION
    assert entity.id == '2'

    assert not stop_time_update.departure.time
    assert not stop_time_update.arrival.time

    assert stop_time_update.Extensions[
        intersection_gtfs_realtime.intersection_stop_time_update].\
               scheduled_arrival.time == 1702924920
    assert stop_time_update.Extensions[
        intersection_gtfs_realtime.intersection_stop_time_update].\
               scheduled_departure.time == 1702924920


def test_mnmt_route_short_name_with_terminal(mnmt):
    translator = MnmtGtfsRealtimeTranslator()
    message = translator(mnmt)

    entity = message.entity[0]
    trip_update = entity.trip_update

    assert message.header.gtfs_realtime_version == FeedMessage.VERSION
    assert entity.id == '1'

    assert trip_update.Extensions[
               intersection_gtfs_realtime.intersection_trip_update].\
               route_short_name == '22A'


def test_mnmt_route_short_name_without_terminal(mnmt):
    translator = MnmtGtfsRealtimeTranslator()
    message = translator(mnmt)

    entity = message.entity[1]
    trip_update = entity.trip_update

    assert message.header.gtfs_realtime_version == FeedMessage.VERSION
    assert entity.id == '2'

    assert trip_update.Extensions[
               intersection_gtfs_realtime.intersection_trip_update].\
               route_short_name == '22'


def test_mnmt_headsign(mnmt):
    translator = MnmtGtfsRealtimeTranslator()
    message = translator(mnmt)

    entity = message.entity[0]
    trip_update = entity.trip_update

    assert message.header.gtfs_realtime_version == FeedMessage.VERSION
    assert entity.id == '1'

    assert trip_update.Extensions[
               intersection_gtfs_realtime.intersection_trip_update].headsign \
           == 'Brklyn Ctr Tc / N Lyndale / Via Penn Av'
