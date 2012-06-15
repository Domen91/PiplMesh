from collections import defaultdict 
from urllib import urlopen

from xml.dom import minidom
from xml.dom.minidom import parseString

from django.db import models
from django.utils.translation import ugettext_lazy as _

from piplmesh.panels.horoscope.models import Horoscope
from piplmesh.panels.horoscope.models import HOROSCOPE_SIGNS

HOROSCOPE_SIGNS_DICT = dict(HOROSCOPE_SIGNS)

def get_horoscope_sign(day, month):
    """
    Based on date, returns horoscope sign key.
    """

    if month == 3:
        if day > 20:
            return 'aries'
        else:
            return 'pisces'
    elif month == 4:
        if day > 20:
            return 'taurus'
        else:
            return 'aries'
    elif month == 5:
        if day > 21:
            return 'gemini'
        else:
            return 'taurus'
    elif month == 6:
        if day > 21:
            return 'cancer'
        else:
            return 'gemini'
    elif month == 7:
        if day > 23:
            return 'leo'
        else:
            return 'cancer'
    elif month == 8:
        if day > 23:
            return 'virgo'
        else:
            return 'leo'
    elif month == 9:
        if day > 23:
            return 'libra'
        else:
            return 'virgo'
    elif month == 10:
        if day > 23:
            return 'scorpio'
        else:
            return 'libra'
    elif month == 11:
        if day > 22:
            return 'sagittarius'
        else:
            return 'scorpio'
    elif month == 12:
        if day > 22:
            return 'capricorn'
        else:
            return 'sagittarius'
    elif month == 1:
        if day < 20:
            return 'aquarius'
        else:
            return 'capricorn'
    elif month == 2:
        if day > 19:
            return 'pisces'
        else:
            return 'aquarius'

def get_all_horoscopes():
    """
    Returns all avaiable horoscopes.
    """

    return HOROSCOPES

class HoroscopeBase(object):
    """
    Parent class for defined horoscope methods for getting horoscope in your language.
    """

    @classmethod
    def get_supported_languages(cls):
        """
        Returns dict of supported languages.
        """

        languages = []
        for object in HOROSCOPES:
            language = object.get_language()
            if language not in languages:
                languages.append(language)
        return languages

    @classmethod
    def get_horoscope(cls, language, sign):
        """
        Returns horoscope data depend on languages and sign.
        """

        for object in HOROSCOPES:
            h_language = object.get_language()
            if language == h_language:
                return object.fetch_data(sign)

class EnglishHoroscope(HoroscopeBase):
    """
    Daily english horoscope from http://findyourfate.com
    """

    language = 'en'

    def get_language(self):
        return self.language

    def fetch_data(self, sign):
        request_sign = {
            'aries' : 'Aries',
            'pisces': 'Pisces',
            'taurus': 'Taurus',
            'gemini': 'Gemini',
            'cancer': 'Cancer',
            'leo': 'Leo',
            'virgo': 'Virgo',
            'libra': 'Libra',
            'scorpio': 'Scorpio',
            'sagittarius': 'Sagittarius',
            'capricorn': 'Capricorn',
            'aquarius': 'Aquarius',
        }

        source = "http://findyourfate.com"
        source_xml = "%s/rss/dailyhoroscope-feed.asp?sign=%s" % (source, request_sign[sign])

        url_xml_open = urlopen(source_xml)
        horoscope_xml = url_xml_open.read()

        date = parseString(horoscope_xml).getElementsByTagName('title')[1].toxml()
        date = date.replace('<title>'+request_sign[sign]+' Horoscope for ', '').replace('</title>', '')

        description = parseString(horoscope_xml).getElementsByTagName('description')[1].toxml()
        description = description.replace('<description>', '').replace('</description>', '')
        url_xml_open.close()

        return (description, sign, source, date)

class SlovenianHoroscope(HoroscopeBase):
    """
    Daily slovenian horoscope from http://slovenskenovice.si
    """

    language = 'sl'

    def get_language(self):
        return self.language

    def fetch_data(self, sign):
        request_sign = {
            'aries' : 'oven',
            'pisces': 'ribi',
            'taurus': 'bik',
            'gemini': 'dvojcka',
            'cancer': 'rak',
            'leo': 'lev',
            'virgo': 'devica',
            'libra': 'tehtnica',
            'scorpio': 'skorpijon',
            'sagittarius': 'strelec',
            'capricorn': 'kozorog',
            'aquarius': 'vodnar',
        }

        source = "http://www.slovenskenovice.si"
        source_xml = "%s/lifestyle/astro/%s" % (source, request_sign[sign])
        open_url = urlopen(source_xml)

        horoscope_xml = open_url.read()

        search_start_date = '<span class="views-label views-label-field-horoscope-content-general">HOROSKOP ZA '
        search_end_date = ': </span>    <strong class="field-content">'

        index_line_date = horoscope_xml.find(search_start_date)
        index_start_date = index_line_date+len(search_start_date)
        index_end_date = horoscope_xml.find(search_end_date)
        date = horoscope_xml[index_start_date:index_end_date]

        search_start_string = '<strong class="field-content">'
        search_end_string = '</strong>  </div>  </div>'

        index_line = horoscope_xml.find(search_start_string)
        index_start = index_line+len(search_start_string)
        index_end = horoscope_xml.find(search_end_string)
        horoscope = horoscope_xml[index_start:index_end]

        return (horoscope, sign, source, date)

HOROSCOPES = (
    EnglishHoroscope(),
    SlovenianHoroscope(),
)