import warnings

from gtfs_realtime_translators.translators import LaMetroGtfsRealtimeTranslator, \
    SeptaRegionalRailTranslator, MtaSubwayGtfsRealtimeTranslator, NjtRailGtfsRealtimeTranslator, \
    CtaSubwayGtfsRealtimeTranslator, CtaBusGtfsRealtimeTranslator, PathGtfsRealtimeTranslator, \
    SwiftlyGtfsRealtimeTranslator, WcdotGtfsRealTimeTranslator, NjtBusGtfsRealtimeTranslator


class TranslatorKeyWarning(Warning):
    pass


class TranslatorRegistry:
    TRANSLATORS = {
        'la-metro': LaMetroGtfsRealtimeTranslator,
        'septa-regional-rail': SeptaRegionalRailTranslator,
        'septa': SwiftlyGtfsRealtimeTranslator,
        'cta-subway': CtaSubwayGtfsRealtimeTranslator,
        'cta-bus': CtaBusGtfsRealtimeTranslator,
        'mta-subway': MtaSubwayGtfsRealtimeTranslator,
        'njt-rail': NjtRailGtfsRealtimeTranslator,
        'njt-bus': NjtBusGtfsRealtimeTranslator,
        'path': PathGtfsRealtimeTranslator,
        'vta': SwiftlyGtfsRealtimeTranslator,
        'wcdot-bus': WcdotGtfsRealTimeTranslator,
    }

    @classmethod
    def get(cls, key):
        if key in cls.TRANSLATORS:
            return cls.TRANSLATORS[key]
        else:
            warnings.warn(f'No translator registered for key={key}', TranslatorKeyWarning)
