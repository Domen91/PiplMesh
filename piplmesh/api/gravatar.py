# import libs for encoding urls and generating md5 hash
import urllib, hashlib

# avatar function which return URL to avatar picture
def gravatarURL(email, size = 40, default = STATIC_URL+piplmesh/images/+"avatar.png"):
	# construct the url
	gravatarUrl = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
	gravatarUrl += urllib.urlencode({'d':default, 's':str(size)})
	
	return gravatarUrl
	
# avatar function which return IMG tag to avatar picture
def gravatarImgTag(email, size = 40, default = "avatar.png"):
	url = avatarUrl(email = email, size = size, defualt = default)
	imgTagUrl = "<img src=" + url + "\" border=\"0\" />";
	
	return imgTagUrl
	
