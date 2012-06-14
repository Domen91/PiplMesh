from django.utils.translation import ugettext_lazy as _

from urllib import urlopen
from xml.dom import minidom
from xml.dom.minidom import parseString

from django.db import models
from mongoengine import *
from mongoengine.django import *

from piplmesh.panels.horoscope import models

def get_horoscope_mark_string(mark):
    """
    Return translated horoscope marks.
    """

    horoscope_marks = [_("Aries"), _("Pisces"), _("Taurus"), _("gemini"), _("Cancer"), _("Leo"), _("Virgo"), _("Libra"), _("Scorpio"), _("Sagittarius"), _("Capricorn"), _("Aquarius")]
    return horoscope_marks[mark]

def get_horoscope_available_languages():
    """
    Return available horoscope languages.
    If we create a new function for get horoscope in a new languages, we must add language in below list.
    """

    available_languages = ['en', 'sl']
    return available_languages

def get_horoscope_mark(day, month):
    """
    Function return horoscope mark number.
    Returnd numbers:
        0 - Aries
        1 - Pisces
        2 - Taurus
        3 - Gemini
        4 - Cancer
        5 - Leo
        6 - Virgo
        7 - Libra
        8 - Scorpio
        9 - Sagittarius
        10 - Capricon
        11 - Aquarius
    """

    if month == 3:
        if day > 20:
            return 0
        else:
            return 1
    elif month == 4:
        if day > 20:
            return 2
        else:
            return 0
    elif month == 5:
        if day > 21:
            return 3
        else:
            return 2
    elif month == 6:
        if day > 21:
            return 4
        else:
            return 3
    elif month == 7:
        if day > 23:
            return 5
        else:
            return 4
    elif month == 8:
        if day > 23:
            return 6
        else:
            return 5
    elif month == 9:
        if day > 23:
            return 7
        else:
            return 6
    elif month == 10:
        if day > 23:
            return 8
        else:
            return 7
    elif month == 11:
        if day > 22:
            return 9
        else:
            return 8
    elif month == 12:
        if day > 22:
            return 10
        else:
            return 9
    elif month == 1:
        if day < 20:
            return 11
        else:
            return 10
    elif month == 2:
        if day > 19:
            return 1
        else:
            return 11

def get_daily_horoscope(user_object):
    """
    Return horoscope mark, description for today's horoscope and a source
    """

    user_language = user_object.language
    
    if user_object.birthdate:
        day = user_object.birthdate.day
        month = user_object.birthdate.month

        user_mark = get_horoscope_mark(day, month)

        horoscope = models.Horoscope.objects(
            mark=user_mark,
            language=user_language 
        )

        if horoscope:
            horoscope = horoscope[0]
            return (horoscope.description, get_horoscope_mark_string(user_mark), horoscope.source)
        else:
            (desc, user_mark, src) = celery_horoscope_update(user_mark, user_language)
            try:
                desc = desc.encode("utf-8")
            except UnicodeError:
                desc = unicode(desc, "utf-8")

            models.Horoscope(language=user_language, mark=user_mark, description=desc, source=src).save()

            return (desc, get_horoscope_mark_string(user_mark), src)

    return (_("Error getting horoscope."), _("None"), "")

def celery_horoscope_update(mark, lang):
    """
    Function returned horoscope from source site.
    If we create a new function for get horoscope in a new languages, we must add a if statmenet below.
    """

    if lang == 'sl':
        return get_daily_slovene_horoscope(mark)

    return get_daily_english_horoscope(mark)

def get_daily_english_horoscope(mark):
    """
    Daily english horoscope from http://findyourfate.com
    """

    request_mark = ['Aries', 'Pisces', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius']

    source = "http://findyourfate.com"
    source_xml = "%s/rss/dailyhoroscope-feed.asp?sign=%s" % (source, request_mark[mark])

    url_xml_open = urlopen(source_xml)
    horoscope_xml = url_xml_open.read()

    description = parseString(horoscope_xml).getElementsByTagName('description')[1].toxml()
    description = description.replace('<description>', '').replace('</description>', '')
    url_xml_open.close()

    return (description, mark, source)

def get_daily_slovene_horoscope(mark):
    """
    Daily slovenian horoscope from http://slovenskenovice.si
    """
    
    request_mark = ['oven', 'ribi', 'bik', 'dvojcka', 'rak', 'lev', 'devica', 'tehtnica', 'skorpijon', 'strelec', 'kozorog', 'vodnar']

    source = "http://www.slovenskenovice.si"
    source_xml = "%s/lifestyle/astro/%s" % (source, request_mark[mark])
    open_url = urlopen(source_xml)

    horoscope_xml = open_url.read()

    search_start_string = '<strong class="field-content">'
    search_end_string = '</strong>  </div>  </div>'

    index_line = horoscope_xml.find(search_start_string)
    index_start = index_line+len(search_start_string)
    index_end = horoscope_xml.find(search_end_string)
    horoscope = horoscope_xml[index_start:index_end]

    return (horoscope, mark, source)
