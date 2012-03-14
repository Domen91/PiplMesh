from django.views import generic as generic_views
from django.conf import settings

class HomeView(generic_views.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        context.update({
            'search_engine': 'Google',
            'search_engine_logo': 'google_logo.png',
			'facebook_authentication_ID': settings.FACEBOOK_ID,
			'facebook_script' : 'facebook.js',
        })

        return context
