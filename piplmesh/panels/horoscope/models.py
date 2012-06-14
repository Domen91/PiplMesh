from django.db import models

import mongoengine
from mongoengine import Document

from piplmesh import settings

class Horoscope(Document):
    sign = mongoengine.StringField() #TODO: add choices=piplmesh.panels.horoscope.horoscope.HOROSCOPE_SIGN - return error
    language = mongoengine.StringField(choices=settings.LANGUAGES)
    description = mongoengine.StringField()
    source = mongoengine.StringField()
    date = mongoengine.StringField()
