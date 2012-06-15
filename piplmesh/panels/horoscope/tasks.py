from celery import task

from django.utils.encoding import smart_unicode

from piplmesh.panels.horoscope import horoscope
from piplmesh.panels.horoscope.models import Horoscope

@task.task
def update_horoscope():
    update_all_horoscope()

def update_all_horoscope():
    """
    Function for updating all languages avaiable horoscope.
    """

    for horoscope_object in horoscope.get_all_horoscopes():
        for sign in map(lambda s: s, horoscope.HOROSCOPE_SIGNS_DICT):
            h_lang = horoscope_object.get_language()

            (h_desc, h_sign, h_src, h_date) = horoscope_object.fetch_data(sign)

            insert_update_one_horoscope(h_lang, h_desc, h_sign, h_src, h_date)

def insert_update_one_horoscope(h_lang, h_desc, h_sign, h_src, h_date):
    """
    Update if exsits otherwise insert a new.
    """

    h_lang=smart_unicode(h_lang)
    h_desc=smart_unicode(h_desc)
    h_sign=smart_unicode(h_sign)
    h_src=smart_unicode(h_src)
    h_date=smart_unicode(h_date)

    # Try update, if failed insert a new object
    if not Horoscope.objects(language=h_lang, sign=h_sign).update(set__description=h_desc, set__source=h_src, set__date=h_date):
        Horoscope(language=h_lang, sign=h_sign, description=h_desc, source=h_src, date=h_date).save()
