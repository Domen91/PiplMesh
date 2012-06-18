from __future__ import absolute_import

from django.utils import translation
from django.utils.translation import ugettext_lazy as _

from piplmesh import panels
from . import horoscope, models

class HoroscopePanel(panels.BasePanel):
    def get_context(self, context):
        user = context['user']

        horoscope_forecast = ''
        horoscope_source_name = ''
        horoscope_source_url = ''
        horoscope_sign = ''
        horoscope_date = ''
        horoscope_date_string = ''

        if user.birthdate == None:
            context.update({
                'header': _("Today's horoscope"),
                'error_birthdate': True,
            })
            return context

        if translation.get_language() not in horoscope.get_supported_languages():
            context.update({
                'header': _("Today's horoscope"),
                'error_language': True,
            })
            return context

        user_sign = horoscope.get_horoscope_sign(user.birthdate.day, user.birthdate.month)

        horoscope_object = models.Horoscope.objects(
            sign = user_sign,
            language = user.language
        )

        if not horoscope_object:
            context.update({
                'header': _("Today's horoscope"),
                'error_data': True,
            })
            return context

        horoscope_forecast = horoscope_object[0].forecast
        horoscope_source_name = horoscope.get_horoscope_provider(user.language).get_source_name()
        horoscope_source_url = horoscope.get_horoscope_provider(user.language).get_source_url()
        horoscope_sign = horoscope.HOROSCOPE_SIGNS_DICT[user_sign]
        horoscope_date = horoscope_object[0].date

        horoscope_date_string = "%s.%s.%s" % (horoscope_date.day, horoscope_date.month, horoscope_date.year)

        context.update({
            'horoscope_forecast': horoscope_forecast,
            'horoscope_sign': horoscope_sign,
            'horoscope_date': horoscope_date_string,
            'horoscope_source_name': horoscope_source_name,
            'horoscope_source_url': horoscope_source_url,
        })

        return context

panels.panels_pool.register(HoroscopePanel)
