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
        print(trip_updates)
        return FeedMessage.create(entities=trip_updates)
    
    def generate_trip_updates(self,entities):
        trip_updates = []
        for entity in entities:
            current_trip_update = self.process_trip_update(entity['trip_update'])
            if(current_trip_update):
                trip_update = TripUpdate.create(
                entity_id = entity.get('id'),
                arrival_delay = current_trip_update.get('arrival_delay'),
                departure_delay = current_trip_update.get('departure_delay'),
                trip_id = current_trip_update.get('trip_id'),
                route_id = current_trip_update.get('route_id'),
                stop_id = self.stop_id
            )
                trip_updates.append(current_trip_update)
        return trip_updates

    def process_trip_update(self,trip_update):
        current_trip_update = {}
        should_process = True
        trip_id, route_id = self.get_trip_info(trip_update.get('trip'))
        current_trip_update.__setitem__('trip_id', trip_id)
        current_trip_update.__setitem__('route_id', route_id)
        arrival_delay, departure_delay = self.get_stop_time_update(trip_update.get('stop_time_update'))
        if(arrival_delay == 999 and departure_delay == 999):
           should_process = False
        current_trip_update.__setitem__('arrival_delay',arrival_delay)
        current_trip_update.__setitem__('departure_delay',departure_delay)
        if(should_process == False):
            return None
        return current_trip_update

    def get_trip_info(self,trip):
        trip_id = trip.get("trip_id")
        route_id = trip.get("route_id")
        return trip_id, route_id

    def get_stop_time_update(self,stop_time_updates):
        arrival_delay_default = 999
        departure_delay_default = 999
        if len(stop_time_updates) == 0:
            return arrival_delay_default,departure_delay_default
        for update in stop_time_updates:
            has_present_stop_id = update.get("stop_id") == self.stop_id
            if has_present_stop_id:
                arrival_delay = update.get('arrival').get('delay')
                departure_delay = update.get('departure').get('delay')
                return arrival_delay,departure_delay
            else:
                continue
        return arrival_delay_default,departure_delay_default
