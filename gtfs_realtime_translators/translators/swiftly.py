import json
import math

import pendulum

from gtfs_realtime_translators.factories import TripUpdate, FeedMessage
from gtfs_realtime_translators.validators import RequiredFieldValidator


class SwiftlyGtfsRealtimeTranslator:
    AGENCY_TIMEZONE_MAP = {
        'lametro': 'America/Los_Angeles',
        'septa': 'America/New_York',
    }

    def __init__(self, stop_id=None):
        RequiredFieldValidator.validate_field_value('stop_id', stop_id)
        self.stop_id = stop_id

    def __call__(self, data):
        json_data = json.loads(data)
        entities = []
        agency_key = json_data.get("agencyKey", None)
        timezone = self.__get_timezone(agency_key)
        for data in json_data["data"]["predictionsData"]:
            stop_id = data.get("stopId", None)
            RequiredFieldValidator.validate_field_value('stop_id', stop_id)
            trip_updates = self.__make_trip_updates(data, stop_id, timezone)
            entities.extend(trip_updates)

        return FeedMessage.create(entities=entities)

    @classmethod
    def __make_trip_updates(cls, data, stop_id, timezone):
        trip_updates = []
        route_id = data.get("routeId")

        # Intersection Extensions
        route_short_name = data.get("routeShortName")
        route_long_name = data.get("routeName")
        stop_name = data.get("stopName")

        for destination in data["destinations"]:
            # Intersection Extension
            headsign = destination.get("headsign")
            direction_id = int(destination.get("directionId", -1))
            # realtime predictions
            predictions = enumerate(destination["predictions"])
            for _idx, arrival in predictions:
                entity_id = str(_idx + 1)
                now = int(pendulum.now().timestamp())
                arrival_or_departure_time = now + \
                    math.floor(arrival.get("sec") / 60) * 60
                trip_id = arrival.get('tripId')

                trip_update = TripUpdate.create(entity_id=entity_id,
                                                arrival_time=arrival_or_departure_time,
                                                departure_time=arrival_or_departure_time,
                                                trip_id=trip_id,
                                                route_id=route_id,
                                                route_short_name=route_short_name,
                                                route_long_name=route_long_name,
                                                stop_id=stop_id,
                                                stop_name=stop_name,
                                                headsign=headsign,
                                                direction_id=direction_id,
                                                agency_timezone=timezone
                                                )

                trip_updates.append(trip_update)

        return trip_updates

    @classmethod
    def __get_timezone(cls, agency_key):
        if not agency_key:
            return None
        return cls.AGENCY_TIMEZONE_MAP.get(agency_key, None)
