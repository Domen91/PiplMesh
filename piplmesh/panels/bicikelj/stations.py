import urllib2
from datetime import datetime, timedelta
from django.utils import timezone

from lxml import objectify

from piplmesh import settings
from . import models

BICIKELJ_STATIONS_URL = 'http://www.bicikelj.si/service/carto'
BICIKELJ_INFO_URL = 'http://www.bicikelj.si/service/stationdetails/ljubljana/%d'
STALE_DATA_TIME = 10

# A comment explaining how to calculate map bounds, so we can search for stations visible on map only
#
# BOUNDS_LATITUDE and BOUNDS_LONGITUDE are the distance between a node and top location of the map
# and the distance between a node and leftmost location of the map, respectively
# BOUNDS_LATITUDE = map_height*0.703119412486786/2^map_zoom
# BOUNDS_LONGITUDE = map_width*0.703119412486786/2^map_zoom

BICIKELJ_BOUNDS_LATITUDE = 0.00557895
BICIKELJ_BOUNDS_LONGITUDE = 0.00557895

def get_stations_nearby(latitude, longitude):
    stations_nearby_all = models.BicikeljStation.objects(
        location__near = (latitude, longitude),
        location__within_box = ((latitude-BICIKELJ_BOUNDS_LATITUDE,longitude-BICIKELJ_BOUNDS_LONGITUDE),(latitude+BICIKELJ_BOUNDS_LATITUDE,longitude+BICIKELJ_BOUNDS_LONGITUDE)),
        fetch_time__gt = timezone.now() - timedelta(seconds=STALE_DATA_TIME*settings.POLL_BICIKELJ_INTERVAL),
    )
    if not stations_nearby_all:
        return
    newest_station = stations_nearby_all[0]
    for station in stations_nearby_all[1:]:
        if station.station_id != newest_station.station_id:
            newest_station.old_data = newest_station.fetch_time < timezone.now() - timedelta(seconds=2*settings.POLL_BICIKELJ_INTERVAL)
            yield newest_station
            newest_station = station
        elif station.fetch_time > newest_station.fetch_time:
            newest_station = station
    newest_station.old_data = newest_station.fetch_time < timezone.now() - timedelta(seconds=2*settings.POLL_BICIKELJ_INTERVAL)
    yield newest_station
    # TODO: check if some stations nearby have data older than 10 minutes. Then display just their names, without current information

def fetch_data():
    stations_tree = objectify.fromstring(urllib2.urlopen(BICIKELJ_STATIONS_URL).read())
    for node in stations_tree.markers.marker:
        info_data = objectify.fromstring(urllib2.urlopen(BICIKELJ_INFO_URL % int(node.attrib['number'])).read())
        yield {
                'station_id': int(node.attrib['number']),
                'timestamp': datetime.fromtimestamp(int(info_data.updated)),
                'name': node.attrib['name'],
                'address': node.attrib['address'],
                'location': (float(node.attrib['lat']), float(node.attrib['lng'])),
                'available': int(info_data.available),
                'free': int(info_data.free),
                'total': int(info_data.total),
                'open': bool(info_data.open),
                'fetch_time': timezone.now(),
        }