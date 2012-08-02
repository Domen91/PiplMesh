from __future__ import absolute_import

from celery import task

from . import models, providers

@task.task
def update_horoscope():
    """
    Function for updating all languages avaiable horoscope.
    Update if exists otherwise insert a new.
    """

    for horoscope_provider in providers.get_all_providers():
        for sign in models.HOROSCOPE_SIGNS_DICT:
            horoscope_data = horoscope_provider.fetch_data(sign)

            models.Horoscope.objects(language=horoscope_provider.get_language(), sign=sign, date=horoscope_data['date']).update(set__forecast=horoscope_data['forecast'], upsert=True)