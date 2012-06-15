from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

import mongoengine
from mongoengine import Document

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

class Horoscope(Document):
    sign = mongoengine.StringField(choices=HOROSCOPE_SIGNS)
    language = mongoengine.StringField(choices=settings.LANGUAGES)
    description = mongoengine.StringField()
    source = mongoengine.StringField()
    date = mongoengine.StringField()
