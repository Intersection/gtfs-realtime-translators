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
        route_id_lookup = {'#D93A30': '862',
                           '#4D92FB,#FF9900': '1024',
                           '#FF9900': '861'}

        stop_id_lookup = {'862_NWK_NWK': '781719',
                          '862_NWK_HAR': '781721',
                          '862_EXP_HAR': '781721',
                          '862_NWK_JSQ': '781725',
                          '862_EXP_JSQ': '781725',
                          '862_NWK_GRV': '781727',
                          '862_EXP_GRV': '781727',
                          '862_NWK_EXP': '781731',
                          '862_EXP_EXP': '781731',
                          '862_NWK_WTC': '794724',
                          '862_WTC_NWK': '781718',
                          '862_WTC_HAR': '781720',
                          '862_WTC_JSQ': '781722',
                          '862_WTC_GRV': '781726',
                          '862_WTC_EXP': '781730',
                          '862_WTC_WTC': '794724'}

        # linecolor_considered_station_target
        arrivals = data['results']
        for arrival in arrivals:
            arrival_updates = arrival['messages']
            for update in arrival_updates:
                try:
                    route_id = route_id_lookup[update['lineColor']]
                    # print(route_id)
                    destination = arrival['target']
                    # print(destination)
                    station = arrival['consideredStation']
                    # print(station)

                    # create the key for the stopId lookup
                    key = route_id + '_' + destination + '_' + station
                    # print(key)
                    stop_id = stop_id_lookup[key]
                    print(stop_id)
                except KeyError:
                    pass

        trip_updates = []

        return trip_updates
