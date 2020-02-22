import json

from gtfs_realtime_translators.factories import FeedMessage


class PathGtfsRealtimeTranslator:
    TIMEZONE = 'America/New_York'

    """
        lineColor => [route_id, targets]
        targets => {WTC => {consideredStation => stopId}, NWK => {consideredStation => stopId}}
        
        target = lineColor[targets[data[<target>]]
        stopId = target[data[<consideredStation>]]
        routeId = lineColor[<route_id>]
        arrival_time = data[<secondsToArrival>]
        headsign = data[<headsign>]
        custom_status = data[<arrivalTimeMessage>]
    """

    def __call__(self, data):
        json_data = json.loads(data)
        entities = self.__make_trip_updates(json_data)
        return FeedMessage.create(entities=entities)

    @classmethod
    def __make_trip_updates(cls, data):
        print(data)
        trip_updates = []

        return trip_updates
