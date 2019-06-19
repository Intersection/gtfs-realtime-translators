# gtfs-realtime-translators

[![Build Status](https://travis-ci.org/Intersection/gtfs-realtime-translators.svg?branch=master)](https://travis-ci.org/Intersection/gtfs-realtime-translators) [![Total alerts](https://img.shields.io/lgtm/alerts/g/Intersection/gtfs-realtime-translators.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Intersection/gtfs-realtime-translators/alerts/) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Intersection/gtfs-realtime-translators.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Intersection/gtfs-realtime-translators/context:python)

`gtfs-realtime-translators` translates custom arrivals formats to GTFS-realtime. It uses the Google [`gtfs-realtime-bindings`](https://github.com/google/gtfs-realtime-bindings/tree/master/python) for Python, supplemented by Intersection extensions.

## Overview

Following the [GTFS-realtime spec](https://developers.google.com/transit/gtfs-realtime/), its three pillars are:
- `TripUpdate`
- `VehiclePosition`
- `Alert`

A `FeedMessage` is a list of _entities_, each of which is one of the types above. A `FeedMessage` may have entities of different types.

As of 2019-06-15, only `TripUpdate` is supported.

## Installation
```
pip install -e git+https://github.com/Intersection/gtfs-realtime-translators.git@<TAG>#egg=gtfs-realtime-translators
```

## Usage

### Registry
The registry is used to return a translator for a given translator key. This is useful to decouple the translator lookup via external systems from its implementation.
```
from gtfs_realtime_translators.registry import TranslatorRegistry

translator_klass = TranslatorRegistry.get('la-metro')
translator = translator_klass(input_data, **kwargs)
```

### Translators
```
from gtfs_realtime_translators.translators import LaMetroGtfsRealtimeTranslator

translator = LaMetroGtfsRealtimeTranslator(la_metro_rail_input_data, stop_id='80122')
feed_message = translator.feed_message
feed_bytes = translator.serialize()
```

### Factories
New translators should be contributed back to this library.
```
from gtfs_realtime_translators.factories import TripUpdate, FeedMessage

trip_update = TripUpdate.create(entity_id=entity_id,
                                arrival_time=arrival_time,
                                departure_time=departure_time,
                                trip_id=trip_id,
                                stop_id=stop_id,
                                route_id=route_id)

entities = [ trip_update ]

feed_message = FeedMessage.create(entities=entities)
```

## GTFS-Realtime Bindings

### Source `gtfs-realtime.proto`
The GTFS-realtime spec is maintained in the [google/transit](https://github.com/google/transit.git) repository. Currently, since there is no versioned way to programmatically include this in our projects, we must clone it as a manual dependency.
```
git clone https://github.com/google/transit.git ../google-transit
cp ../google-transit/gtfs-realtime/proto/gtfs-realtime.proto gtfs_realtime_translators/bindings/
```

### Re-generate Bindings
For our Python libraries to understand the interface specified by the GTFS-realtime spec, we must generate language bindings.
```
virtualenv ~/.env/gtfs-realtime-bindings
source ~/.env/gtfs-realtime-bindings/bin/activate
pip install grpcio-tools
python3 -m grpc_tools.protoc -I gtfs_realtime_translators/bindings/ --python_out=gtfs_realtime_translators/bindings/ gtfs_realtime_translators/bindings/intersection.proto
```
Since we are using the published spec bindings, we must do one more step. Inside the generated file, `gtfs_realtime_translators/bindings/intersection_pb2.py`, change the following line
```
import gtfs_realtime_pb2 as gtfs__realtime__pb2
```
to
```
from google.transit import gtfs_realtime_pb2 as gtfs__realtime__pb2
```

## Run Tests Locally

```
pip install -r requirements.txt
pip install -e .
pytest
```
