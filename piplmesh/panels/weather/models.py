from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

import mongoengine

class Weather(mongoengine.Document):
    date = mongoengine.DateTimeField(required=True)
    date_current = mongoengine.StringField(required=True)
    date_tomorrow = mongoengine.StringField(required=True)
    date_after_tomorrow = mongoengine.StringField(required=True)
    latitude = mongoengine.DecimalField(required=True)
    longitude = mongoengine.DecimalField(required=True)
    temperature_current = mongoengine.DecimalField(required=True)
    temperature_tomorrow= mongoengine.DecimalField(required=True)
    temperature_after_tomorrow= mongoengine.DecimalField(required=True)
    weathericon_current = mongoengine.IntField(required=True)
    weathericon_tomorrow = mongoengine.IntField(required=True)
    weathericon_after_tomorrow = mongoengine.IntField(required=True)