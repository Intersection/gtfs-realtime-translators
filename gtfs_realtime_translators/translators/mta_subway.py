import math

import pendulum

from gtfs_realtime_translators.factories import TripUpdate, FeedMessage


class MtaSubwayGtfsRealtimeTranslator:
    def __init__(self, data, stop_id=None):
        entities = []
        for group in data["groups"]:
            for idx, arrival in enumerate(group["times"]):
                route_id = group['route']['id']
                stop_id = data['stop']['id']
                entities.append(self.__make_trip_update(idx, route_id, arrival))

        self.feed_message = FeedMessage.create(entities=entities)

    @classmethod
    def __make_trip_update(cls, _id, route_id, arrival):
        entity_id = str(_id + 1)
        arrival_time = arrival['serviceDay'] + arrival['realtimeArrival']
        departure_time = arrival['serviceDay'] + arrival['realtimeDeparture']
        trip_id = arrival['tripId']
        route_id = route_id
        stop_id = arrival['stopId']

        ##### Intersection Extensions
        headsign = arrival['tripHeadsign']
        track = arrival['track']
        scheduled_arrival_time = arrival['serviceDay'] + arrival['scheduledArrival']
        scheduled_departure_time = arrival['serviceDay'] + arrival['scheduledDeparture']
        return TripUpdate.create(entity_id=entity_id,
                                arrival_time=arrival_time,
                                departure_time=departure_time,
                                trip_id=trip_id,
                                route_id=route_id,
                                stop_id=stop_id,
                                headsign=headsign,
                                track=track,
                                scheduled_arrival_time=scheduled_arrival_time,
                                scheduled_departure_time=scheduled_departure_time)


    def serialize(self):
        return self.feed_message.SerializeToString()
