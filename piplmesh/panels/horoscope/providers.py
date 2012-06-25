from __future__ import absolute_import

import datetime, re, urllib

from xml.dom import minidom

from django.utils import encoding

from . import models

HOROSCOPE_SIGNS_DICT = dict(models.HOROSCOPE_SIGNS)

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

def get_all_providers():
    """
    Returns all avaiable horoscopes.
    """

    return HOROSCOPE_PROVIDERS

def get_provider(language):
    """
    Returns an instance of the horoscope provider for requested language, or raises ``KeyError`` if it does not exist.
    """

    for horoscope in get_all_providers():
        if horoscope.get_language() == language:
            return horoscope

    raise KeyError("Unsupported language: '%s'" % language)

def get_supported_languages():
    """
    Returns a list of supported languages (their language codes).

    That is, a list of languages provided by defined horoscope providers.
    """

    languages = []
    for horoscope in get_all_providers():
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
        return NotImplementedError

class EnglishHoroscope(HoroscopeProviderBase):
    """
    Daily english horoscope from http://findyourfate.com.
    """

    language = 'en'
    source_name = 'Find your fate'
    source_url = 'http://findyourfate.com/'

    provider_sign_names = {
        'aries': 'Aries',
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
    
    provider_month_names = {
        'January': 'January',
        'February': 'February',
        'March': 'March',
        'April': 'April',
        'May': 'May',
        'June': 'June',
        'July': 'July',
        'August': 'August',
        'September': 'September',
        'October': 'October',
        'November': 'November',
        'December': 'December',
    }

    def fetch_data(self, sign):
        horoscope_url = '%srss/dailyhoroscope-feed.asp?sign=%s' % (self.source_url, self.provider_sign_names[sign])
        horoscope_xml = minidom.parse(urllib.urlopen(horoscope_url))

        return {
            'date': self.date_parsing(horoscope_xml, sign),
            'forecast': encoding.smart_unicode(self.forecast_parsing(horoscope_xml)),
        }

    def date_parsing(self, xml, sign):
        date_string_text = xml.getElementsByTagName('title')[1].firstChild.data
        date_string_text = date_string_text.replace(self.provider_sign_names[sign] + ' Horoscope for ', '')
        date_string_day = re.findall(r'\d{1,2}', date_string_text)[0]
        date_string_month = re.sub('[0-9, ]', '', re.sub(r'\w{5,10}, ', '', date_string_text))
        date_string_year = re.findall(r'\d{4}', date_string_text)[0]
        date_string = '%s. %s %s' % (date_string_day, self.provider_month_names[date_string_month], date_string_year)
        date = datetime.datetime.strptime(date_string, '%d. %B %Y')

        return date

    def forecast_parsing(self, xml):
        return xml.getElementsByTagName('description')[1].firstChild.data

class SlovenianHoroscope(HoroscopeProviderBase):
    """
    Daily slovenian horoscope from http://slovenskenovice.si.
    """

    language = 'sl'
    source_name = 'Slovenske novice'
    source_url = 'http://www.slovenskenovice.si/'

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
        horoscope_url = '%slifestyle/astro/%s' % (self.source_url, self.provider_sign_names[sign])
        horoscope_xml = urllib.urlopen(horoscope_url).read()

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
        }

HOROSCOPE_PROVIDERS = (
    EnglishHoroscope(),
    SlovenianHoroscope(),
)
