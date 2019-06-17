from collections.abc import Iterable

from google.transit import gtfs_realtime_pb2 as gtfs_realtime

from gtfs_realtime_translators.factories import TripUpdate, FeedMessage


def test_models_schema_output():
    entity_id = '1'
    arrival_time = 1234
    trip_id = '1234'
    stop_id = '2345'
    route_id = '3456'

    trip_update = TripUpdate.create(entity_id=entity_id,
                                    arrival_time=arrival_time,
                                    trip_id=trip_id,
                                    stop_id=stop_id,
                                    route_id=route_id)

    entities = [ trip_update ]
    message = FeedMessage.create(entities=entities)

    assert type(message) == gtfs_realtime.FeedMessage
    assert type(message.header) == gtfs_realtime.FeedHeader
    assert isinstance(message.entity, Iterable)
    assert len(message.entity) == 1

    entity = message.entity[0]
    assert type(entity) == gtfs_realtime.FeedEntity

    trip_update = entity.trip_update
    assert type(trip_update) == gtfs_realtime.TripUpdate
    assert isinstance(trip_update.stop_time_update, Iterable)
    assert len(trip_update.stop_time_update) == 1
    assert isinstance(trip_update.trip, gtfs_realtime.TripDescriptor)

    stop_time_update = trip_update.stop_time_update[0]
    assert type(stop_time_update) == gtfs_realtime.TripUpdate.StopTimeUpdate
    assert type(stop_time_update.arrival) == gtfs_realtime.TripUpdate.StopTimeEvent
    assert type(stop_time_update.departure) == gtfs_realtime.TripUpdate.StopTimeEvent

def test_departure_time_is_used_if_available():
    entity_id = '1'
    arrival_time = 1234
    departure_time = 2345
    trip_id = '1234'
    stop_id = '2345'
    route_id = '3456'

    entity = TripUpdate.create(entity_id=entity_id,
                               arrival_time=arrival_time,
                               departure_time=departure_time,
                               trip_id=trip_id,
                               stop_id=stop_id,
                               route_id=route_id)

    assert entity.trip_update.stop_time_update[0].arrival.time == arrival_time
    assert entity.trip_update.stop_time_update[0].departure.time == departure_time

def test_arrival_time_is_used_if_no_departure_time():
    entity_id = '1'
    arrival_time = 1234
    trip_id = '1234'
    stop_id = '2345'
    route_id = '3456'

    entity = TripUpdate.create(entity_id=entity_id,
                               arrival_time=arrival_time,
                               trip_id=trip_id,
                               stop_id=stop_id,
                               route_id=route_id)

    assert entity.trip_update.stop_time_update[0].arrival.time == arrival_time
    assert entity.trip_update.stop_time_update[0].departure.time == arrival_time
