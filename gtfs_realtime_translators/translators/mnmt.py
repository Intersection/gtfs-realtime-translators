import json

import pendulum

from gtfs_realtime_translators.factories import TripUpdate, FeedMessage


class MnmtGtfsRealtimeTranslator:
    TIMEZONE = 'America/Chicago'

    def __call__(self, data):
        json_data = json.loads(data)

        stops_list = json_data.get('stops')
        departures_list = json_data.get('departures')

        entities = []
        if stops_list and departures_list:
            entities = self.__make_trip_updates(stops_list, departures_list)

        return FeedMessage.create(entities=entities)

    @classmethod
    def __make_trip_updates(cls, stops_list, departures_list):
        trip_updates = []
        stop_name = stops_list[0].get("description")

        for index, departure in enumerate(departures_list):
            entity_id = str(index + 1)

            trip_id = departure.get('trip_id')

            stop_id = departure.get('stop_id')
            if stop_id:
                stop_id = str(stop_id)

            headsign = departure.get('description')
            route_id = departure.get('route_id')
            route_short_name = departure.get('route_short_name')
            direction_id = departure.get('direction_id')

            departure_time, scheduled_departure_time = None, None
            if cls.__is_realtime_departure(departure):
                departure_time = departure.get('departure_time')
            else:
                scheduled_departure_time = departure.get('departure_time')
            trip_update = TripUpdate.create(entity_id=entity_id,
                                            departure_time=departure_time,
                                            scheduled_departure_time=scheduled_departure_time,
                                            trip_id=trip_id,
                                            route_id=route_id,
                                            route_short_name=route_short_name,
                                            stop_id=stop_id,
                                            stop_name=stop_name,
                                            headsign=headsign,
                                            direction_id=direction_id,
                                            agency_timezone=cls.TIMEZONE
                                            )

            trip_updates.append(trip_update)

        return trip_updates

    @classmethod
    def __is_realtime_departure(cls, departure):
        return departure.get('actual') is True
