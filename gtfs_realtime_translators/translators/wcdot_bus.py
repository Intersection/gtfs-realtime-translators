import json
from gtfs_realtime_translators.factories import TripUpdate, FeedMessage
from gtfs_realtime_translators.validators import RequiredFieldValidator


class WcdotGtfsRealTimeTranslator:
    TIMEZONE = 'America/New_York'

    def __init__(self, stop_id=None):
        RequiredFieldValidator.validate_field_value('stop_id', stop_id)
        self.stop_id = stop_id
        self.filtered_stops = None

    def __call__(self,data):
        json_data = json.loads(data)
        entities = json_data["entity"]
        trip_updates = self.generate_trip_updates(entities)
        return FeedMessage.create(entities=trip_updates)

    def generate_trip_updates(self, entities):
        trip_updates = []
        for idx, entity in enumerate(entities):
            entity_id = str(idx+1)
            trip_update = entity['trip_update']
            trip = trip_update.get('trip')
            trip_id = trip.get('trip_id')
            route_id = trip.get('route_id')
            if route_id:
                route_id = route_id.lstrip('0')
            stop_time_update = trip_update.get('stop_time_update')
            for update in stop_time_update:
                stop_id = update.get("stop_id")
                arrival = update.get("arrival")
                departure = update.get("departure")
                if stop_id == self.stop_id:
                    arrival_delay = None
                    departure_delay = None
                    if arrival:
                        arrival_delay = arrival.get('delay',None)
                    if departure:
                        departure_delay = departure.get('delay',None)
                    trip_update = TripUpdate.create(
                        entity_id=entity_id,
                        arrival_delay=arrival_delay,
                        departure_delay=departure_delay,
                        trip_id=trip_id,
                        route_id=route_id,
                        stop_id=stop_id,
                        agency_timezone=self.TIMEZONE
                    )
                    trip_updates.append(trip_update)
        return trip_updates
