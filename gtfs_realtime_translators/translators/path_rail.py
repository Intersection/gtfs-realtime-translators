

class PathGtfsRealtimeTranslator:
    TIMEZONE = 'America/New_York'

    """
        lineColor => [route_id, targets]
        targets => {WTC => {consideredStation => stopId}, NWK => {consideredStation => stopId}}
        
        target = lineColor[targets[data[<target>]]
        stopId = target[data[<consideredStation>]]
        routeId = lineColor[<route_id>]
        arrival_time = data[<secondsToArrival>]
        headsign = data[<headsign>]
        custom_status = data[<arrivalTimeMessage>]
    """
    pass
