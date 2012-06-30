from __future__ import absolute_import

from celery import task

from piplmesh.panels.weather import weather as weather_functions

from . import weather, models

@task.task
def update_weather():
    for weather in models.Weather.objects:
        weather_data = weather_functions.fetch_data(weather.latitude,weather.longitude)
        weather.update(
            set__date=str(weather_data['date']),
            set__date_current=str(weather_data['date_current']),
            set__date_tomorrow=str(weather_data['date_tomorrow']),
            set__date_after_tomorrow=str(weather_data['date_after_tomorrow']),
            set__latitude=str(weather_data['latitude']),
            set__longitude=str(weather_data['longitude']),
            set__temperature_current=str(weather_data['temperature_current']),
            set__temperature_tomorrow=str(weather_data['temperature_tomorrow']),
            set__temperature_after_tomorrow=str(weather_data['temperature_after_tomorrow']),
            set__weathericon_current=str(weather_data['weathericon_current']),
            set__weathericon_tomorrow=str(weather_data['weathericon_tomorrow']),
            set__weathericon_after_tomorrow=str(weather_data['weathericon_after_tomorrow'])
            )
            
def insert_weather(lat,longitude):
    
    '''if weather for place not exist insert it'''
       
    if models.Weather.objects(latitude=str(lat),longitude=str(longitude)).count()==0:
        weather_data = weather_functions.fetch_data(lat,longitude)
        models.Weather(
            date=weather_data['date'],
            date_current=weather_data['date_current'],
            date_tomorrow=weather_data['date_tomorrow'],
            date_after_tomorrow=weather_data['date_after_tomorrow'],
            latitude=weather_data['latitude'],
            longitude=weather_data['longitude'],
            temperature_current=weather_data['temperature_current'],
            temperature_tomorrow=weather_data['temperature_tomorrow'],
            temperature_after_tomorrow=weather_data['temperature_after_tomorrow'],
            weathericon_current=weather_data['weathericon_current'],
            weathericon_tomorrow=weather_data['weathericon_tomorrow'],
            weathericon_after_tomorrow=weather_data['weathericon_after_tomorrow']
        ).save()