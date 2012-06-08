from django.utils.translation import ugettext_lazy as _

from urllib import urlopen
from xml.dom import minidom
from xml.dom.minidom import parseString

def get_horoscope_mark(day, month):
    """
    Function return translated horoscope mark.
    """

    if month == 3:
        if day > 20:
            return _("Aries")
        else:
            return _("Pisces")
    elif month == 4:
        if day > 20:
            return _("Taurus")
        else:
            return _("Aries")
    elif month == 5:
        if day > 21:
            return _("Gemini")
        else:
            return _("Taurus")
    elif month == 6:
        if day > 21:
            return _("Cancer")
        else:
            return _("Gemini")
    elif month == 7:
        if day > 23:
            return _("Leo")
        else:
            return _("Cancer")
    elif month == 8:
        if day > 23:
            return _("Virgo")
        else:
            return _("Leo")
    elif month == 9:
        if day > 23:
            return _("Libra")
        else:
            return _("Virgo")
    elif month == 10:
        if day > 23:
            return _("Scorpio")
        else:
            return _("Libra")
    elif month == 11:
        if day > 22:
            return _("Sagittarius")
        else:
            return _("Scorpio")
    elif month == 12:
        if day > 22:
            return _("Capricon")
        else:
            return _("Sagittarius")
    elif month == 1:
        if day < 20:
            return _("Aquarius")
        else:
            return _("Capricon")
    elif month == 2:
        if day > 19:
            return _("Pisces")
        else:
            return _("Aquarius")

def get_daily_english_horoscope(day, month):
    """
    Daily english horoscope from http://findyourfate.com
    """

    # Used _proxy___args[0] otherwise return an error
    mark = get_horoscope_mark(day, month)._proxy____args[0]
    source = "http://findyourfate.com"
    source_xml = "%s/rss/dailyhoroscope-feed.asp?sign=%s" % (source, mark)

    url_xml_open = urlopen(source_xml)
    horoscope_xml = url_xml_open.read()
    description = parseString(horoscope_xml).getElementsByTagName('description')[1].toxml()
    description = description.replace('<description>', '').replace('</description>', '')
    url_xml_open.close()

    return (description, mark, source)

def get_daily_slovene_horoscope(day, month):
    """
    Daily slovenian horoscope from http://slovenskenovice
    
    For working slovenian horoscope, you must translated horoscope mark to correct slovenian languages!
    """

    mark = get_horoscope_mark(day, month)
    mark_decode = mark.lower()

    # Get correct url name for parsing
    if mark_decode[1:] == 'korpijon':
        mark_decode='skorpijon'
    elif mark_decode[0:4] == 'dvoj':
        mark_decode='dvojcka'

    source = "http://www.slovenskenovice.si"
    source_xml = source + "/lifestyle/astro/%s" % mark_decode
    open_url = urlopen(source_xml)

    horoscope_xml = open_url.read()

    search_start_string = '<strong class="field-content">'
    search_end_string = '</strong>  </div>  </div>'

    index_line = horoscope_xml.find(search_start_string)
    index_start = index_line+len(search_start_string)
    index_end = horoscope_xml.find(search_end_string)
    horoscope = horoscope_xml[index_start:index_end]

    if len(horoscope) > 500:
        return get_daily_english_horoscope(day, month)
    return (horoscope, mark, source)

def get_daily_horoscope(user_object):
    """
    Return horoscope mark, description for today's horoscope and a source
    """

    language = user_object.language

    day = user_object.birthdate.day
    month = user_object.birthdate.month

    if language == 'sl':
        return get_daily_slovene_horoscope(day, month)
    return get_daily_english_horoscope(day, month)
