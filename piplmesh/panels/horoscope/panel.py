from django.utils.translation import ugettext_lazy as _

from piplmesh import panels
from piplmesh.panels.horoscope import horoscope
from piplmesh.panels.horoscope.models import Horoscope
from piplmesh.panels.horoscope.tasks import insert_update_one_horoscope

class HoroscopePanel(panels.BasePanel):
    def get_context(self, context):
        user=context['user']

        horoscope_description = ""
        horoscope_source = ""
        horoscope_sign = ""
        horoscope_date = ""

        if user.birthdate and user.language in horoscope.HoroscopeBase.get_supported_languages():
            user_sign = horoscope.get_horoscope_sign(user.birthdate.day, user.birthdate.month)

            horoscope_object = Horoscope.objects(
                sign=user_sign,
                language=user.language
            )

            if horoscope_object:
                horoscope_description = horoscope_object[0].description
                horoscope_source = horoscope_object[0].source
                horoscope_sign = horoscope.HOROSCOPE_SIGNS_DICT[horoscope_object[0].sign]
                horoscope_date = horoscope_object[0].date
            else:
                (horoscope_description, horoscope_sign, horoscope_source, horoscope_date) = horoscope.HoroscopeBase.get_horoscope(user.language, user_sign)
                insert_update_one_horoscope(user.language, horoscope_description, horoscope_sign, horoscope_source, horoscope_date)

                horoscope_sign=horoscope.HOROSCOPE_SIGNS_DICT[horoscope_sign]
        else:
            horoscope_sign = _("Horoscope is unavailable in your language.")

        context.update({
            'header': _("Today's horoscope"),
            'horoscope_description': horoscope_description,
            'horoscope_sign': horoscope_sign,
            'horoscope_date': horoscope_date,
            'horoscope_source': horoscope_source,
        })

        return context

panels.panels_pool.register(HoroscopePanel)
