import warnings

from gtfs_realtime_translators.translators import LaMetroGtfsRealtimeTranslator, \
    SeptaRegionalRailTranslator, MtaSubwayGtfsRealtimeTranslator, NjtRailGtfsRealtimeTranslator, \
    CtaSubwayGtfsRealtimeTranslator, CtaBusGtfsRealtimeTranslator, PathGtfsRealtimeTranslator, \
    PathNewGtfsRealtimeTranslator, SwiftlyGtfsRealtimeTranslator, WcdotGtfsRealTimeTranslator, \
    NjtBusGtfsRealtimeTranslator, MbtaGtfsRealtimeTranslator, MnmtGtfsRealtimeTranslator, \
    MartaRailGtfsRealtimeTranslator


class TranslatorKeyWarning(Warning):
    pass


class TranslatorRegistry:
    TRANSLATORS = {
        'la-metro-old': LaMetroGtfsRealtimeTranslator,
        'septa-regional-rail': SeptaRegionalRailTranslator,
        'cta-subway': CtaSubwayGtfsRealtimeTranslator,
        'cta-bus': CtaBusGtfsRealtimeTranslator,
        'mta-subway': MtaSubwayGtfsRealtimeTranslator,
        'njt-rail': NjtRailGtfsRealtimeTranslator,
        'njt-bus': NjtBusGtfsRealtimeTranslator,
        'path-old': PathGtfsRealtimeTranslator,
        'path-new': PathNewGtfsRealtimeTranslator,
        'swiftly': SwiftlyGtfsRealtimeTranslator,
        'wcdot-bus': WcdotGtfsRealTimeTranslator,
        'mbta': MbtaGtfsRealtimeTranslator,
        'mnmt': MnmtGtfsRealtimeTranslator,
        'marta-rail': MartaRailGtfsRealtimeTranslator
    }

    @classmethod
    def get(cls, key):
        if key in cls.TRANSLATORS:
            return cls.TRANSLATORS[key]
        else:
            warnings.warn(f'No translator registered for key={key}', TranslatorKeyWarning)
