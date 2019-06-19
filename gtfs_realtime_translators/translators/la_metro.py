import math

import pendulum

from gtfs_realtime_translators.factories import TripUpdate, FeedMessage


class LaMetroGtfsRealtimeTranslator:
    def __init__(self, data, stop_id=None):
        entities = [ self.__make_trip_update(idx, stop_id, arrival) for idx, arrival in enumerate(data['items']) ]
        self.feed_message = FeedMessage.create(entities=entities)

    @classmethod
    def calculate_trip_id(cls, trip_id):
        """
        Trip IDs from LA Metro often come in the form <static_trip_id>_<date_string>.
        We must parse the static_trip_id only.
        """
        try:
            return trip_id.split('_')[0]
        except Exception:
            return trip_id

    @classmethod
    def __make_trip_update(cls, _id, stop_id, arrival):
        entity_id = str(_id + 1)
        now = int(pendulum.now().timestamp())
        arrival_time = now + math.floor(arrival['seconds'] / 60) * 60
        trip_id = cls.calculate_trip_id(arrival['trip_id'])

        return TripUpdate.create(entity_id=entity_id,
                                 arrival_time=arrival_time,
                                 trip_id=trip_id,
                                 stop_id=stop_id)


    def serialize(self):
        return self.feed_message.SerializeToString()
