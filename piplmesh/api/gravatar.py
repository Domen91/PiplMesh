# import libs for encoding urls and generating md5 hash
import urllib, hashlib

# avatar function which return URL to avatar picture
def gravatarURL(email, size = 40):
	# construct the url
	gravatarUrl = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
	gravatarUrl += urllib.urlencode({'s':str(size)})

	return gravatarUrl