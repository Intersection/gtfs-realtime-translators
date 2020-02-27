import json
import math
import warnings

import pendulum

from gtfs_realtime_translators.factories import FeedMessage, TripUpdate


class PathGtfsRealtimeTranslatorWarning(Warning):
    pass


class PathGtfsRealtimeTranslator:
    TIMEZONE = 'America/New_York'

    ROUTE_ID_LOOKUP = {
        '#4D92FB': '859',
        '#65C100': '860',
        '#FF9900': '861',
        '#D93A30': '862',
        '#4D92FB,#FF9900': '1024'}

    STOP_ID_LOOKUP = {
        '859_33S_HOB': '781715',
        '859_33S_CHR': '781732',
        '859_33S_09S': '781734',
        '859_33S_14S': '781736',
        '859_33S_23S': '781738',
        '859_33S_33S': '781740',
        '859_HOB_HOB': '781717',
        '859_HOB_CHR': '781733',
        '859_HOB_09S': '781735',
        '859_HOB_14S': '781737',
        '859_HOB_23S': '781739',
        '859_HOB_33S': '781741',
        '860_HOB_HOB': '781715',
        '860_HOB_NEW': '781728',
        '860_HOB_EXP': '781731',
        '860_HOB_WTC': '781763',
        '860_WTC_HOB': '781716',
        '860_WTC_NEW': '781729',
        '860_WTC_EXP': '781730',
        '860_WTC_WTC': '781763',
        '861_33S_JSQ': '781723',
        '861_33S_GRV': '781726',
        '861_33S_NEW': '781728',
        '861_33S_CHR': '781732',
        '861_33S_09S': '781734',
        '861_33S_14S': '781736',
        '861_33S_23S': '781738',
        '861_33S_33S': '781740',
        '861_JSQ_JSQ': '781724',
        '861_JSQ_GRV': '781727',
        '861_JSQ_NEW': '781729',
        '861_JSQ_CHR': '781733',
        '861_JSQ_09S': '781735',
        '861_JSQ_14S': '781737',
        '861_JSQ_23S': '781739',
        '861_JSQ_33S': '781741',
        '862_NWK_NWK': '781719',
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
        '862_EXP_NWK': '781718',
        '862_WTC_HAR': '781720',
        '862_WTC_JSQ': '781722',
        '862_WTC_GRV': '781726',
        '862_WTC_EXP': '781730',
        '862_WTC_WTC': '794724',
        '1024_33S_HOB': '781715',
        '1024_33S_JSQ': '781723',
        '1024_33S_GRV': '781726',
        '1024_33S_NEW': '781728',
        '1024_33S_CHR': '781732',
        '1024_33S_09S': '781734',
        '1024_33S_14S': '781736',
        '1024_33S_23S': '781738',
        '1024_33S_33S': '781740',
        '1024_JSQ_HOB': '781716',
        '1024_JSQ_JSQ': '781724',
        '1024_JSQ_GRV': '781727',
        '1024_JSQ_NEW': '781729',
        '1024_JSQ_CHR': '781733',
        '1024_JSQ_09S': '781735',
        '1024_JSQ_14S': '781737',
        '1024_JSQ_23S': '781739',
        '1024_JSQ_33S': '781741'
    }

    """
       Since PATH GTFS data have stops that are, in most cases, unique to a route, direction, service date, and/or 
       destination, a mapping is created to ensure we return the appropriate stop_id for a station's arrival updates.
       
       Keys are based off the line color (a hex value that can be mapped to a GTFS route_id), the destination, and the 
       current station for which the request has been made.
    """

    def __call__(self, data):
        json_data = json.loads(data)
        entities = self.__make_trip_updates(json_data)
        return FeedMessage.create(entities=entities)

    @classmethod
    def __make_trip_updates(cls, data):
        trip_updates = []
        now = int(pendulum.now().timestamp())

        arrivals = data['results']
        for arrival in arrivals:
            arrival_updates = arrival['messages']
            for idx, update in enumerate(arrival_updates):
                try:
                    route_id = cls.ROUTE_ID_LOOKUP[update['lineColor']]
                    destination = arrival['target']
                    station = arrival['consideredStation']

                    key = route_id + '_' + destination + '_' + station
                    stop_id = cls.STOP_ID_LOOKUP[key]
                    arrival_time = now + math.floor(update['secondsToArrival'] / 60) * 60
                    headsign = update['headSign']

                    trip_update = TripUpdate.create(entity_id=str(idx + 1),
                                                    departure_time=arrival_time,
                                                    arrival_time=arrival_time,
                                                    route_id=route_id,
                                                    stop_id=stop_id,
                                                    headsign=headsign)
                    trip_updates.append(trip_update)
                except KeyError:
                    warnings.warn(f'Could not generate trip_update for update [{update}] in arrival [{arrival}]',
                                  PathGtfsRealtimeTranslatorWarning)

        return trip_updates
