import json

import pendulum

from gtfs_realtime_translators.factories import TripUpdate, FeedMessage


class CtaSubwayGtfsRealtimeTranslator:
    TIMEZONE = 'America/Chicago'

    def __init__(self, **kwargs):
        stop_list = kwargs.get('stop_list')
        if stop_list:
            self.stop_list = stop_list.split(',')
        else:
            self.stop_list = None

    def __call__(self, data):
        json_data = json.loads(data)
        predictions = json_data['ctatt']['eta']

        entities = []
        for idx, prediction in enumerate(predictions):
            stop_id = prediction['stpId']
            if not self.stop_list or stop_id in self.stop_list:
                entities.append(self.__make_trip_update(idx, prediction))

        return FeedMessage.create(entities=entities)


    @classmethod
    def __to_unix_time(cls, time):
        return pendulum.parse(time).in_tz(cls.TIMEZONE).int_timestamp

    @classmethod
    def __make_trip_update(cls, _id, prediction):
        entity_id = str(_id + 1)
        route_id = prediction['rt']
        stop_id = prediction['stpId']

        is_scheduled = prediction['isSch'] == '1'
        parsed_arrival_time = cls.__to_unix_time(prediction['arrT'])
        arrival_time = None if is_scheduled else parsed_arrival_time

        ##### Intersection Extensions
        headsign = prediction['destNm']
        scheduled_arrival_time = parsed_arrival_time if is_scheduled else None

        parsed_prediction_time = cls.__to_unix_time(prediction['prdt'])
        custom_status = cls.__get_custom_status(parsed_arrival_time,
                                                parsed_prediction_time)
        scheduled_interval = cls.__get_scheduled_interval(is_scheduled,
                                                          prediction['schInt'])

        route_icon = cls.__get_route_icon(prediction['flags'], headsign)
        run_number = int(prediction['rn'])

        return TripUpdate.create(entity_id=entity_id,
                                 route_id=route_id,
                                 stop_id=stop_id,
                                 arrival_time=arrival_time,
                                 headsign=headsign,
                                 scheduled_arrival_time=scheduled_arrival_time,
                                 custom_status=custom_status,
                                 agency_timezone=cls.TIMEZONE,
                                 scheduled_interval=scheduled_interval,
                                 route_icon=route_icon,
                                 run_number=run_number)

    @classmethod
    def __get_custom_status(cls, arrival_time, prediction_time):
        minutes_until_train_arrives = (arrival_time - prediction_time) / 60
        if minutes_until_train_arrives <= 1:
            return 'DUE'
        return f'{round(minutes_until_train_arrives)} min'

    @classmethod
    def __get_scheduled_interval(cls, is_scheduled, scheduled_interval):
        if is_scheduled:
            scheduled_interval_seconds = int(scheduled_interval) * 60
            return scheduled_interval_seconds
        return None

    @classmethod
    def __get_route_icon(cls, flags, headsign):
        if flags and flags.lower() == 'h':
            return 'holiday'
        if headsign and headsign.lower() in ["midway", "o'hare"]:
            return 'airport'
        return None
