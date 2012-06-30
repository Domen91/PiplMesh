from __future__ import absolute_import

from . import models

from django import http
from django.conf import settings
from django.core import urlresolvers
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

from piplmesh import nodes, panels
from piplmesh.panels import weather

class WeatherPanel(panels.BasePanel):
    def get_context(self, context):
        '''todo- get latitude and longitude from request'''
        lat = 50.17
        long = 14.96
        weather.tasks.insert_weather(lat,long)
        weather.tasks.update_weather()
        weather_data = models.Weather.objects(latitude=str(lat),longitude=str(long))[0]
        context.update({
            'header': _("Weather"),
            'date': weather_data['date'],
            'date_current': weather_data['date_current'],
            'date_tomorrow': weather_data['date_tomorrow'],
            'date_after_tomorrow': weather_data['date_after_tomorrow'],
            'latitude': weather_data['latitude'],
            'longitude': weather_data['longitude'],
            'temperature_current': weather_data['temperature_current'],
            'temperature_tomorrow': weather_data['temperature_tomorrow'],
            'temperature_after_tomorrow': weather_data['temperature_after_tomorrow'],
            'weathericon_current': weather_data['weathericon_current'],
            'weathericon_tomorrow': weather_data['weathericon_tomorrow'],
            'weathericon_after_tomorrow': weather_data['weathericon_after_tomorrow'],
        })

        return context
    
panels.panels_pool.register(WeatherPanel)