import pytest

from gtfs_realtime_translators.translators import LaMetroGtfsRealtimeTranslator, \
        SeptaRegionalRailTranslator, \
        SwiftlyGtfsRealtimeTranslator, \
        CtaSubwayGtfsRealtimeTranslator, \
        CtaBusGtfsRealtimeTranslator, \
        MtaSubwayGtfsRealtimeTranslator, \
        NjtRailGtfsRealtimeTranslator, \
        NjtBusGtfsRealtimeTranslator, \
        PathGtfsRealtimeTranslator, \
        PathNewGtfsRealtimeTranslator, \
        WcdotGtfsRealTimeTranslator, \
        MbtaGtfsRealtimeTranslator
from gtfs_realtime_translators.registry import TranslatorRegistry, TranslatorKeyWarning

def test_registry_for_valid_key():
    assert TranslatorRegistry.get('la-metro-old') == LaMetroGtfsRealtimeTranslator
    assert TranslatorRegistry.get('septa-regional-rail') == SeptaRegionalRailTranslator
    assert TranslatorRegistry.get('septa') == SwiftlyGtfsRealtimeTranslator
    assert TranslatorRegistry.get('cta-subway') == CtaSubwayGtfsRealtimeTranslator
    assert TranslatorRegistry.get('cta-bus') == CtaBusGtfsRealtimeTranslator
    assert TranslatorRegistry.get('mta-subway') == MtaSubwayGtfsRealtimeTranslator
    assert TranslatorRegistry.get('njt-rail') == NjtRailGtfsRealtimeTranslator
    assert TranslatorRegistry.get('njt-bus') == NjtBusGtfsRealtimeTranslator
    assert TranslatorRegistry.get('path-old') == PathGtfsRealtimeTranslator
    assert TranslatorRegistry.get('path-new') == PathNewGtfsRealtimeTranslator
    assert TranslatorRegistry.get('swiftly') == SwiftlyGtfsRealtimeTranslator
    assert TranslatorRegistry.get('wcdot-bus') == WcdotGtfsRealTimeTranslator
    assert TranslatorRegistry.get('mbta') == MbtaGtfsRealtimeTranslator

def test_registry_for_invalid_key():
    with pytest.warns(TranslatorKeyWarning):
        TranslatorRegistry.get('unknown-translator')
