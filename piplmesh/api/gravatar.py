import urllib, hashlib
from django.contrib.sites.models import Site

from settings import *

def gravatarURL(email, size = 50, ssl = 'on', default = 'unknown.png'):
	""" GravatarURL function return URL image, depends on user email."""

	sites = Site.objects.get_current()

	if ssl == "on":
		http = "https"
	else:
		http = "http"

	# Construct the url for default avatar and gravatar services
	defaultAvatarUrl = "%(http)s://%(site)s%(static)spiplmesh/images/%(avatar)s" % {"http": http, "site": sites.domain, "static": STATIC_URL, "avatar": default}
	emailHash = hashlib.md5(email.lower()).hexdigest()
	gravatarUrl = "%(http)s://www.gravatar.com/avatar/%(emailHash)s?s=%(size)d&d=%(defaultAvatar)s" % {"http": http, "emailHash": emailHash, "size": size, "defaultAvatar": defaultAvatarUrl}

	return gravatarUrl
