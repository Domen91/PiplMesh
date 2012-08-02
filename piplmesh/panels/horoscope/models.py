from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import mongoengine

HOROSCOPE_SIGNS = (
    ('aries', _("Aries")),
    ('pisces', _("Pisces")),
    ('taurus', _("Taurus")),
    ('gemini', _("Gemini")),
    ('cancer', _("Cancer")),
    ('leo', _("Leo")),
    ('virgo', _("Virgo")),
    ('libra', _("Libra")),
    ('scorpio', _("Scorpio")),
    ('sagittarius', _("Sagittarius")),
    ('capricorn', _("Capricorn")),
    ('aquarius', _("Aquarius")),
)

HOROSCOPE_SIGNS_DICT = dict(HOROSCOPE_SIGNS)

class Horoscope(mongoengine.Document):
    sign = mongoengine.StringField(choices=HOROSCOPE_SIGNS, required=True)
    language = mongoengine.StringField(choices=settings.LANGUAGES, required=True, unique_with=('sign', 'date'))
    forecast = mongoengine.StringField(required=True)
    date = mongoengine.DateTimeField(required=True, unique_with=('sign', 'language'))
