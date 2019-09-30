import json

import pytest
import pendulum

from gtfs_realtime_translators.translators import MtaSubwayGtfsRealtimeTranslator
from gtfs_realtime_translators.factories import FeedMessage

@pytest.fixture
def mta_subway():
    with open('test/fixtures/mta_subway.json') as f:
        raw = json.load(f)

    return raw

def test_mta_subway_data(mta_subway):
    with pendulum.test(pendulum.datetime(2019,2,20,17,0,0)):
        translator = MtaSubwayGtfsRealtimeTranslator(mta_subway, stop_id='MTASBWY:101')

    message = translator.feed_message

    entity = message.entity[0]
    trip_update = entity.trip_update
    stop_time_update = trip_update.stop_time_update[0]

    assert message.header.gtfs_realtime_version == FeedMessage.VERSION

    assert entity.id == '1'

    assert trip_update.trip.trip_id == 'MTASBWY:2351'

    assert stop_time_update.arrival.time == 1569507335
    assert stop_time_update.departure.time == 1569507335
    assert stop_time_update.stop_id == 'MTASBWY:101N'

    feed_bytes = translator.serialize()
    assert type(feed_bytes) == bytes
