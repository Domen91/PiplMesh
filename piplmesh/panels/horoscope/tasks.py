from __future__ import absolute_import

from celery import task

from . import providers, models

@task.task
def update_horoscope():
    """
    Function for updating all languages avaiable horoscope.
    """

    for horoscope_provider in providers.get_all_providers():
        for sign in providers.HOROSCOPE_SIGNS_DICT:
            horoscope_data = horoscope_provider.fetch_data(sign)

            insert_update_one_horoscope(horoscope_data, sign, horoscope_provider.get_language())

def insert_update_one_horoscope(horoscope, sign, language):
    """
    Update if exsits otherwise insert a new.
    """

    # Try update, if failed insert a new object
    if not models.Horoscope.objects(language=language, sign=sign).update(set__forecast=horoscope['forecast'], set__date=horoscope['date']):
        models.Horoscope(language=language, sign=sign, forecast=horoscope['forecast'], date=horoscope['date']).save()
