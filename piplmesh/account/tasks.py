import datetime

from django.conf import settings
from django.utils import timezone

from celery import task

from piplmesh.account import models as account_models
from piplmesh.api import base, models as api_models

@task.task
def clean_inactive_lazy_users():
    users_with_content = []
    for post in api_models.Post.objects:
        users_with_content.append(post.author)
        for comment in post.comments:
            users_with_content.append(comment.author)
    users_with_content = list(set(users_with_content))
    for user in account_models.User.objects:
        if not user.is_authenticated() and (timezone.now() - user.connection_last_unsubscribe).days >= settings.DELETE_LAZY_USER_AFTER_DAYS and user not in users_with_content:
            user.delete()