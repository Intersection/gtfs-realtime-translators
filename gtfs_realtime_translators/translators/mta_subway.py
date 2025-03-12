import json

from gtfs_realtime_translators.factories import TripUpdate, FeedMessage


class MtaSubwayGtfsRealtimeTranslator:
    TIMEZONE = 'America/New_York'

    def __call__(self, data):
        json_data = json.loads(data)
        entities = []
        for stop in json_data:
            for group in stop["groups"]:
                for idx, arrival in enumerate(group["times"]):
                    route_id = self.parse_id(group['route']['id'])
                    stop_name = stop['stop']['name']
                    entities.append(self.__make_trip_update(idx, route_id, stop_name, arrival))

        return FeedMessage.create(entities=entities)

    @classmethod
    def parse_id(cls, value):
        """
        Some values from the MTA Subway feed come in the form MTASBWY:<id>.
        We must parse the id only.
        """
        try:
            return value.split(':')[1]
        except Exception:
            return value

    @classmethod
    def __make_trip_update(cls, _id, route_id, stop_name, arrival):
        entity_id = str(_id + 1)
        arrival_time = arrival['serviceDay'] + arrival['realtimeArrival']
        departure_time = arrival['serviceDay'] + arrival['realtimeDeparture']
        trip_id = cls.parse_id(arrival['tripId'])
        stop_id = cls.parse_id(arrival['stopId'])

        ##### Intersection Extensions
        headsign = arrival['tripHeadsign']
        scheduled_arrival_time = arrival['serviceDay'] + arrival['scheduledArrival']
        scheduled_departure_time = arrival['serviceDay'] + arrival['scheduledDeparture']
        track = arrival.get('track', '')

        return TripUpdate.create(entity_id=entity_id,
                                arrival_time=arrival_time,
                                departure_time=departure_time,
                                trip_id=trip_id,
                                route_id=route_id,
                                stop_id=stop_id,
                                stop_name=stop_name,
                                headsign=headsign,
                                scheduled_arrival_time=scheduled_arrival_time,
                                scheduled_departure_time=scheduled_departure_time,
                                track=track,
                                agency_timezone=cls.TIMEZONE)
