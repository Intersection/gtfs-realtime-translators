import math

import pendulum

from gtfs_realtime_translators.factories import TripUpdate, FeedMessage


class MtaSubwayGtfsRealtimeTranslator:
    def __init__(self, data):
        entities = []
        for stop in data:
            for group in stop["groups"]:
                for idx, arrival in enumerate(group["times"]):
                    route_id = group['route']['id']
                    stop_name = stop['stop']['name']
                    entities.append(self.__make_trip_update(idx, route_id, stop_name, arrival))

        self.feed_message = FeedMessage.create(entities=entities)

    @classmethod
    def get_stop_id(cls, stop_id):
        """
        Stop IDs from MTA Subway  come in the form MTASBY:<stop id>.
        We must parse the stop_id only.
        """
        try:
            return stop_id.split(':')[1]
        except Exception:
            return stop_id


    @classmethod
    def to_gmt_timestamp(cls, timestamp):
        return int(pendulum.from_timestamp(timestamp).subtract(hours=4).timestamp())

    @classmethod
    def __make_trip_update(cls, _id, route_id, stop_name, arrival):
        entity_id = str(_id + 1)
        arrival_time = cls.to_gmt_timestamp(arrival['serviceDay'] + arrival['realtimeArrival'])
        departure_time = cls.to_gmt_timestamp(arrival['serviceDay'] + arrival['realtimeDeparture'])
        trip_id = arrival['tripId']
        route_id = route_id
        stop_id = cls.get_stop_id(arrival['stopId'])
        print(stop_name)

        ##### Intersection Extensions
        headsign = arrival['tripHeadsign']
        scheduled_arrival_time = cls.to_gmt_timestamp(arrival['serviceDay'] + arrival['scheduledArrival'])
        scheduled_departure_time = cls.to_gmt_timestamp(arrival['serviceDay'] + arrival['scheduledDeparture'])
        return TripUpdate.create(entity_id=entity_id,
                                arrival_time=arrival_time,
                                departure_time=departure_time,
                                trip_id=trip_id,
                                route_id=route_id,
                                stop_id=stop_id,
                                stop_name=stop_name,
                                headsign=headsign,
                                scheduled_arrival_time=scheduled_arrival_time,
                                scheduled_departure_time=scheduled_departure_time)


    def serialize(self):
        return self.feed_message.SerializeToString()
