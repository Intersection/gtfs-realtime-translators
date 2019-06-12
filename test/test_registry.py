import pytest

from gtfs_realtime_translators.translators import LaMetroGtfsRealtimeTranslator, \
        SeptaRegionalRailTranslator
from gtfs_realtime_translators.registry import TranslatorRegistry, TranslatorKeyWarning

def test_registry_for_valid_key():
    assert TranslatorRegistry.get('la-metro') == LaMetroGtfsRealtimeTranslator
    assert TranslatorRegistry.get('septa-regional-rail') == SeptaRegionalRailTranslator

def test_registry_for_invalid_key():
    with pytest.warns(TranslatorKeyWarning):
        TranslatorRegistry.get('unknown-translator')
