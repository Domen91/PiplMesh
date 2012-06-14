import datetime
import itertools

from django.conf import settings
from django.utils import timezone

from celery import task

from pushserver.utils import updates

from piplmesh.account import models
from piplmesh.frontend import views

from piplmesh.panels.horoscope import horoscope
from piplmesh.panels.horoscope.models import Horoscope

CHECK_ONLINE_USERS_RECONNECT_TIMEOUT = 2 * settings.CHECK_ONLINE_USERS_INTERVAL

@task.task
def check_online_users():
    for user in models.User.objects(
        is_online=False,
        connections__not__in=([], None), # None if field is missing altogether, not__in seems not to be equal to nin
    ):
        if models.User.objects(
            pk=user.pk,
            is_online=False,
            connections__not__in=([], None), # None if field is missing altogether, not__in seems not to be equal to nin
        ).update(set__is_online=True):
            updates.send_update(
                views.HOME_CHANNEL_ID,
                {
                    'type': 'userlist',
                    'action': 'JOIN',
                    'user': {
                        'username': user.username,
                        'profile_url': user.get_profile_url(),
                        'image_url': user.get_image_url(),
                    },
                }
            )

    for user in models.User.objects(
        is_online=True,
        connections__in=([], None), # None if field is missing altogether
        connection_last_unsubscribe__lt=timezone.now() - datetime.timedelta(seconds=CHECK_ONLINE_USERS_RECONNECT_TIMEOUT),
    ):
        if models.User.objects(
            pk=user.pk,
            is_online=True,
            connections__in=([], None), # None if field is missing altogether
            connection_last_unsubscribe__lt=timezone.now() - datetime.timedelta(seconds=CHECK_ONLINE_USERS_RECONNECT_TIMEOUT),
        ).update(set__is_online=False):
            updates.send_update(
                views.HOME_CHANNEL_ID,
                {
                    'type': 'userlist',
                    'action': 'PART',
                    'user': {
                        'username': user.username,
                        'profile_url': user.get_absolute_url(),
                        'image_url': user.get_image_url(),
                    },
                }
            )

@task.task
def update_horoscope():
    # Get all new horoscope according to available languages and horoscope marks(current it is 12 marks)
    for i_language, i_mark in itertools.product(horoscope.get_horoscope_available_languages(), range(12)):
            # Get new horoscope
            (desc, mark_number, src) = horoscope.celery_horoscope_update(i_mark, i_language)

            try:
                desc = desc.encode("utf-8")
            except UnicodeError:
                desc = unicode(desc, "utf-8")

            # Try update, if failed insert a new object
            if not Horoscope.objects(language=i_language, mark=i_mark).update(set__description=desc, set__source=src):
                Horoscope(language=i_language, mark=i_mark, description=desc, source=src).save()
