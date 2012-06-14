from __future__ import absolute_import

from django.db import models

import mongoengine
from mongoengine import *

class Horoscope(Document):
    mark = mongoengine.IntField()
    language = mongoengine.StringField()
    description = mongoengine.StringField()
    source = mongoengine.StringField()
