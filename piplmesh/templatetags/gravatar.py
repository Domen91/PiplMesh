import urllib, hashlib

from django.contrib.sites import models as sites_models
from django.conf import settings

from django import template

register = template.Library()

@register.inclusion_tag('gravatar.html')
def gravatar(email, size = 50, default = 'unknown.png'):
	"""
		Description: gravatar function return URL image, depends on user email.
		
		Template tag - usage:
		{% load gravatar %}
		{% gravatar "piplmesh@piplmesh" 50 %}
	"""

	if settings.GRAVATAR_HTTPS_DEFAULT:
		http = "https"
	else:
		http = "http"

	site = sites_models.Site.objects.get_current().domain

	# Construct the url for default avatar and gravatar services
	default_avatar_url = "%(http)s://%(site)s%(static)spiplmesh/images/%(avatar)s" % {"http": http, "site": site, "static": settings.STATIC_URL, "avatar": default}
	email_hash = hashlib.md5(email.lower()).hexdigest()
	gravatar_url = "https://secure.gravatar.com/avatar/%(email_hash)s?s=%(size)s&d=%(default_avatar)s" % {"email_hash": email_hash, "size": str(size), "default_avatar": urllib.quote(default_avatar_url)}

	return {'gravatar': {'url': gravatar_url, 'size': size}}