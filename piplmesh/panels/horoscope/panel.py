from __future__ import absolute_import

import datetime

from django.utils import translation
from django.utils.translation import ugettext_lazy as _

from piplmesh import panels

from . import providers, models

class HoroscopePanel(panels.BasePanel):
    def get_context(self, context):
        user = context['user']

        horoscope_forecast = ''
        horoscope_source_name = ''
        horoscope_source_url = ''
        horoscope_sign = ''
        horoscope_date = ''
        horoscope_date_string = ''

        context.update({
            'header': _("Today's horoscope"),
        })

        if not user.birthdate:
            context.update({
                'error_birthdate': True,
            })
            return context

        if translation.get_language() not in providers.get_supported_languages():
            context.update({
                'error_language': True,
            })
            return context

        user_sign = providers.get_horoscope_sign(user.birthdate.day, user.birthdate.month)

        horoscope = models.Horoscope.objects(
            sign = user_sign,
            language = user.language
        )

        if not horoscope:
            context.update({
                'error_data': True,
            })
            return context

        if datetime.datetime.now() > (horoscope[0].date + datetime.timedelta(days=2)):
            context.update({
                'error_date': True,
            })
            return context

        horoscope_forecast = horoscope[0].forecast
        horoscope_source_name = providers.get_provider(user.language).get_source_name()
        horoscope_source_url = providers.get_provider(user.language).get_source_url()
        horoscope_sign = providers.HOROSCOPE_SIGNS_DICT[user_sign]
        horoscope_date = horoscope[0].date

        context.update({
            'horoscope_forecast': horoscope_forecast,
            'horoscope_sign': horoscope_sign,
            'horoscope_date': horoscope_date,
            'horoscope_source_name': horoscope_source_name,
            'horoscope_source_url': horoscope_source_url,
        })

        return context

panels.panels_pool.register(HoroscopePanel)
