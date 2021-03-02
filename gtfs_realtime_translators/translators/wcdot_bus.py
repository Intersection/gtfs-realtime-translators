import json
from gtfs_realtime_translators.factories import TripUpdate, FeedMessage


class WcdotGtfsRealTimeTranslator:
    def __init__(self, stop_id=None):
        if stop_id is None:
            raise ValueError('stop_id is required.')
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
            trip_id = trip_update.get("trip").get('trip_id')
            route_id = trip_update.get("trip").get('route_id')
            stop_time_update = trip_update.get('stop_time_update')

            for update in stop_time_update:
                stop_id = update.get("stop_id")
                if stop_id == self.stop_id:
                    arrival_delay = update.get('arrival').get('delay')
                    departure_delay = update.get('departure').get('delay')
                    trip_update = TripUpdate.create(
                        entity_id=entity_id,
                        arrival_delay=arrival_delay,
                        departure_delay=departure_delay,
                        trip_id=trip_id,
                        route_id=route_id,
                        stop_id=stop_id
                    )
                    trip_updates.append(trip_update)
        return trip_updates
