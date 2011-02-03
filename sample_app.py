from bottle import route, run, request
from instagram import client

CONFIG = {
    'client_id': ''
    'client_secret': ''
    'redirect_uri': 'http://localhost:8515/oauth_callback'
}

unauthenticated_api = client.InstagramAPI(**CONFIG)

@route('/')
def home():
    try:
        url = unauthenticated_api.get_authorize_url()
        return '<a href="%s">Connect with Instagram</a>' % url
    except Exception, e:
        return e

@route('/oauth_callback')
def on_callback():
    code = request.GET.get("code")
    if not code:
        return 'Missing code'
    access_token = unauthenticated_api.exchange_code_for_access_token(code)
    if not access_token:
        return 'Could not get access token'
    
    api = client.InstagramAPI(access_token=access_token)
    recent_media, next = api.user_recent_media()
    photos = []
    for media in recent_media:
        photos.append('<img src="%s"/>' % media.images['thumbnail'].url)
    return ''.join(photos)

run(host='localhost', port=8515)