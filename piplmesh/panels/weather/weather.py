from __future__ import absolute_import

import datetime, re
from urllib import urlopen

from xml.dom import minidom
from xml.dom.minidom import parseString

from django.utils import encoding

from . import models

from xml.dom import minidom

from datetime import datetime, timedelta,date
from time import gmtime, strftime
import time
import urllib

from piplmesh.panels.weather import views
source_url = 'http://api.met.no/'

def fetch_data(latitude, longitude):
    weather_url = '%sweatherapi/locationforecast/1.8/?lat=%s;lon=%s' % (source_url, latitude, longitude)
    weather_xml = minidom.parse(urllib.urlopen(weather_url))

    temperature=[]
    weathericon=[]
    
    try:
        weatherdata  = weather_xml.getElementsByTagName("weatherdata")[0].getElementsByTagName("product")[0].getElementsByTagName("time")

        current_temperature = weatherdata[0].getElementsByTagName("location")[0].getElementsByTagName("temperature")[0]
        temperature.append(current_temperature.attributes["value"].value)

        current_symbol = weatherdata[1].getElementsByTagName("location")[0].getElementsByTagName("symbol")[0]
        weathericon.append(current_symbol.attributes["number"].value)
        
        i=1
        for forecast in weatherdata:
                time_string = str(datetime.now()+timedelta(days = i))
                weather_icon_from = time_string[:10] + "T12:00:00Z"
                weather_icon_to = time_string[:10] + "T18:00:00Z"
                if forecast.attributes["from"].value == weather_icon_to and forecast.attributes["to"].value == weather_icon_to:
                        location_temperature = forecast.getElementsByTagName("location")[0].getElementsByTagName("temperature")[0]
                        temperature.append(location_temperature.attributes["value"].value)
                if forecast.attributes["from"].value == weather_icon_from and forecast.attributes["to"].value == weather_icon_to:
                        location_icon = forecast.getElementsByTagName("location")[0].getElementsByTagName("symbol")[0]
                        weathericon.append(location_icon.attributes["number"].value)
                        i+=1
    
    except:
        raise KeyError("api changed or not working")
    return {
        'date': datetime.now(),
        'date_current': date.today().strftime("%A"),
        'date_tomorrow': time.strftime("%A",time.strptime(str(date.today()+timedelta(days=1)),"%Y-%m-%d")),
        'date_after_tomorrow': time.strftime("%A",time.strptime(str(date.today()+timedelta(days=2)),"%Y-%m-%d")),
        'latitude': latitude,
        'longitude': longitude,
        'temperature_current': temperature[0],
        'temperature_tomorrow': temperature[1],
        'temperature_after_tomorrow': temperature[2],
        'weathericon_current': weathericon[0],
        'weathericon_tomorrow': weathericon[1],
        'weathericon_after_tomorrow': weathericon[2],
        }