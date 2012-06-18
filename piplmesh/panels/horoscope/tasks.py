from __future__ import absolute_import

from celery import task

from . import horoscope, models

@task.task
def update_horoscope():
    """
    Function for updating all languages avaiable horoscope.
    """

    for horoscope_provider in horoscope.get_all_horoscopes_providers():
        for sign in horoscope.HOROSCOPE_SIGNS_DICT:
            horoscope_data = horoscope_provider.fetch_data(sign)

            insert_update_one_horoscope(horoscope_data)

def insert_update_one_horoscope(horoscope):
    """
    Update if exsits otherwise insert a new.
    """

    # Try update, if failed insert a new object
    if not models.Horoscope.objects(language=horoscope['language'], sign=horoscope['sign']).update(set__forecast=horoscope['forecast'], set__date=horoscope['date']):
        models.Horoscope(language=horoscope['language'], sign=horoscope['sign'], forecast=horoscope['forecast'], date=horoscope['date']).save()
