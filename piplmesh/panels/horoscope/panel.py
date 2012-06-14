from django.utils.translation import ugettext_lazy as _

from piplmesh import panels

from horoscope import get_daily_horoscope
 
class HoroscopePanel(panels.BasePanel):
    def get_context(self, context):
        (horoscope_description, horoscope_mark, horoscope_source) = get_daily_horoscope(context['user'])

        context.update({
            'header': _("Today's horoscope"),
            'horoscope_description': horoscope_description,
            'horoscope_mark': horoscope_mark,
            'horoscope_source': horoscope_source,
        })

        return context

panels.panels_pool.register(HoroscopePanel)
