from __future__ import absolute_import

from celery import task

from django.utils.encoding import smart_unicode

from . import horoscope, models

@task.task
def update_horoscope():
    """
    Function for updating all languages avaiable horoscope.
    """

    for horoscope_provider in horoscope.get_all_horoscopes_providers():
        for sign in map(lambda s: s, horoscope.HOROSCOPE_SIGNS_DICT):
            horoscope_language = horoscope_provider.get_language()

            (horoscope_description, horoscope_sign, horoscope_date) = horoscope_provider.fetch_data(sign)

            insert_update_one_horoscope(horoscope_language, horoscope_description, horoscope_sign, horoscope_date)

def insert_update_one_horoscope(horoscope_language, horoscope_description, horoscope_sign, horoscope_date):
    """
    Update if exsits otherwise insert a new.
    """

    horoscope_language = smart_unicode(horoscope_language)
    horoscope_description = smart_unicode(horoscope_description)
    horoscope_sign = smart_unicode(horoscope_sign)

    # Try update, if failed insert a new object
    if not models.Horoscope.objects(language=horoscope_language, sign=horoscope_sign).update(set__description=horoscope_description, set__date=horoscope_date):
        models.Horoscope(language=horoscope_language, sign=horoscope_sign, description=horoscope_description, date=horoscope_date).save()
