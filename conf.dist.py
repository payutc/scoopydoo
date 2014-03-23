# Pour génerer un bon secret :
#     >>> import os
#     >>> os.urandom(24)

APP_KEY = '123'
SECRET = ''
HOSTNAME = 'http://localhost:5000'
PAYUTC_URL = "https://assos.utc.fr/payutc"
PAYUTC_USER_AGENT = 'scoopydoo'

IMPLEMENTED = {
    "BLOCAGE": {"name": "Blocage", "url": "blocage.index"},
    "MESSAGES": {"name": "Messages", "url": "messages.index"},
    "ADMINRIGHT": {"name": "Droits", "url": "droits.index"},
    "GESARTICLE": {"name": "Articles", "url": "articles.index"},
}
