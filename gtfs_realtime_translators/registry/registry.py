import warnings

from gtfs_realtime_translators.translators import LaMetroGtfsRealtimeTranslator, \
        SeptaRegionalRailTranslator

class TranslatorKeyWarning(Warning):
    pass

class TranslatorRegistry:
    TRANSLATORS = {
        'la-metro': LaMetroGtfsRealtimeTranslator,
        'septa-regional-rail': SeptaRegionalRailTranslator,
    }

    @classmethod
    def get(cls, key):
        if key in cls.TRANSLATORS:
            return cls.TRANSLATORS[key]
        else:
            warnings.warn(f'No translator registered for key={key}', TranslatorKeyWarning)
