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
        trip_updates = generate_trip_updates(entities)
        return FeedMessage.create(entities=trip_updates)
        
    def generate_trip_updates(entities):
        trip_updates = []
        for entity in entities:
            current_trip_update = {}
            current_trip_update['entity_id'] = entity['id']
            process_trip_update(entity['trip_update'],current_trip_update)
            trip_update = TripUpdate.create(
                entity_id = current_trip_update['entity_id']
                arrival_delay = current_trip_update['arrival_delay']
                departure_delay = current_trip_update['departure_delay']
                trip_id = current_trip_update['trip_id']
                route_id = current_trip_update['route_id']
                stop_id= self.stop_id
            )
            trip_updates.append(trip_update)
        return trip_updates

    def process_trip_update(trip_update,current_trip_update):
        trip_id, route_id = get_trip_info(trip_update['trip'])
        current_trip_update['trip_id'] = trip_id
        current_trip_update['route_id'] = route_id
        arrival_delay, departure_delay = get_stop_time_update(trip_update['stop_time_update'])
        current_trip_update['arrival_delay'] = arrival_delay
        current_trip_update['departure_delay'] = departure_delay


    def get_trip_info(trip):
        trip_id = trip["trip_id"]
        route_id = trip["route_id"]
        return trip_id, route_id
    
    def get_stop_time_update(stop_time_updates,stop_id):
        if len(trip_updates) == 0:
            return None
        for update in stop_time_updates:
            has_present_stop_id = update["stop_id"] == stop_id
            if has_present_stop_id:
                arrival_delay = update['arrival']['delay']
                departure_delay = update['departure']['delay']
                return arrival_delay,departure_delay
            else:
                continue
           
