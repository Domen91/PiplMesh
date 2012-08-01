from __future__ import absolute_import

import datetime

from django.utils import translation
from django.utils.translation import ugettext_lazy as _

from piplmesh import panels

from . import models, providers

HOROSCOPE_DATE_TOO_OLD = 2

class HoroscopePanel(panels.BasePanel):
    def get_context(self, context):
        user = context['user']

        context.update({
            'header': _("Today's horoscope"),
        })

        if not user.birthdate:
            context.update({
                'error_birthdate': True,
            })
            return context

        try:
            provider = providers.get_provider(translation.get_language())
        except:
            context.update({
                'error_language': True,
            })
            return context

        user_sign = providers.get_horoscope_sign(user.birthdate.day, user.birthdate.month)

        try:
            horoscope = models.Horoscope.objects.get(
                sign = user_sign,
                language = translation.get_language()
            )
        except DoesNotExist:
            context.update({
                'error_data': True,
            })
            return context

        if not horoscope:
            context.update({
                'error_data': True,
            })
            return context

        if datetime.datetime.now() > (horoscope.date + datetime.timedelta(days=HOROSCOPE_DATE_TOO_OLD)):
            context.update({
                'error_obsolete': True,
            })
            return context

        context.update({
            'horoscope_forecast': horoscope.forecast,
            'horoscope_sign': models.HOROSCOPE_SIGNS_DICT[user_sign],
            'horoscope_date': horoscope.date,
            'horoscope_source_name': provider.get_source_name(),
            'horoscope_source_url': provider.get_source_url(),
        })

        return context

panels.panels_pool.register(HoroscopePanel)
