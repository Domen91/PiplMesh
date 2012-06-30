from __future__ import absolute_import

import datetime, re
from urllib import urlopen

from xml.dom import minidom
from xml.dom.minidom import parseString

from django.utils import encoding

from . import models

HOROSCOPE_SIGNS_DICT = dict(models.HOROSCOPE_SIGNS)

def get_all_horoscopes_providers():
    """
    Returns all avaiable horoscopes.
    """

    return HOROSCOPE_PROVIDERS

def get_horoscope_provider(language):
    """
    Returns an instance of the horoscope provider for requested language, or raises ``KeyError`` if it does not exist.
    """

    for horoscope in get_all_horoscopes_providers():
        if horoscope.get_language() == language:
            return horoscope

    raise KeyError("Unsupported language: '%s'" % language)

def get_supported_languages():
    """
    Returns a list of supported languages (their language codes).

    That is, a list of languages provided by defined horoscope providers.
    """

    languages = []
    for horoscope in get_all_horoscopes_providers():
        language = horoscope.get_language()
        assert language not in languages, language
        languages.append(language)
    return languages

class HoroscopeProviderBase(object):
    """
    Base class for horoscope providers.
    """

    language = None
    source_name = None
    source_url = None

    def get_language(self):
        """
        Returns provider's language.
        """

        return self.language

    def get_source_name(self):
        """
        Returns provider's source name.
        """

        return self.source_name

    def get_source_url(self, ):
        """
        Returns provider's source URL.
        """

        return self.source_url

    def fetch_data(self, sign):
        return NotImplemented

class Weather(HoroscopeProviderBase):
	
    source_url = 'http://api.met.no/'

    provider_sign_names = {
        'aries': 'oven',
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

    provider_month_names = {
        'januar': 'January',
        'februar': 'February',
        'marec': 'March',
        'april': 'April',
        'maj': 'May',
        'junij': 'June',
        'julij': 'July',
        'avgust': 'August',
        'september': 'September',
        'oktober': 'October',
        'november': 'November',
        'december': 'December',
    }

    def fetch_data(self, sign):
        horoscope_url = '%sweatherapi/locationforecast/1.8/?lat=%s;lon=%s' % (self.source_url, node.latitude, node.longitude)
        horoscope_xml = urlopen(horoscope_url).read()

        search_start_date = '<span class="views-label views-label-field-horoscope-content-general">HOROSKOP ZA '
        search_end_date = ': </span>    <strong class="field-content">'

        index_line_date = horoscope_xml.find(search_start_date)
        index_start_date = index_line_date+len(search_start_date)
        index_end_date = horoscope_xml.find(search_end_date)
        date_string_html = horoscope_xml[index_start_date:index_end_date]
        date_string_day = re.sub(r'\D', '', date_string_html)
        date_string_month = re.sub('^[0-9\. ]+', '', date_string_html)
        date_string_year = datetime.datetime.now().year
        date_string = '%s. %s %s' % (date_string_day, self.provider_month_names[date_string_month], date_string_year)

        date = datetime.datetime.strptime(date_string, '%d. %B %Y')

        search_start_string = '<strong class="field-content">'
        search_end_string = '</strong>  </div>  </div>'

        index_line = horoscope_xml.find(search_start_string)
        index_start = index_line+len(search_start_string)
        index_end = horoscope_xml.find(search_end_string)
        forecast = horoscope_xml[index_start:index_end]

        return {
            'date': date,
            'forecast': encoding.smart_unicode(forecast),
            'sign': encoding.smart_unicode(sign),
            'language': encoding.smart_unicode(self.language),
        }

HOROSCOPE_PROVIDERS = (
    EnglishHoroscope(),
    SlovenianHoroscope(),
)