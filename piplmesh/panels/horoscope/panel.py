from django.utils.translation import ugettext_lazy as _

from piplmesh import panels

from horoscope import get_daily_horoscope

class HoroscopePanel(panels.BasePanel):
    def get_context(self, context):
        (horoscope_description, horoscope_sign, horoscope_source, horoscope_date) = get_daily_horoscope(context['user'])

        context.update({
            'header': _("Today's horoscope"),
            'horoscope_description': horoscope_description,
            'horoscope_sign': horoscope_sign,
            'horoscope_date': horoscope_date,
            'horoscope_source': horoscope_source,
        })

        return context

panels.panels_pool.register(HoroscopePanel)
