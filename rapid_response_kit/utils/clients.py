from flask import current_app as app
from twilio.rest import TwilioRestClient
from pusher import Pusher


def twilio():
    return TwilioRestClient(app.config['TWILIO_ACCOUNT_SID'],
                            app.config['TWILIO_AUTH_TOKEN'])


def pusher_connect(config=None):
    if config is None:
        config = app.config

    pusher_key = config.get('PUSHER_KEY', None)
    pusher_secret = config.get('PUSHER_SECRET', None)
    pusher_app_id = config.get('PUSHER_APP_ID', None)

    try:
        Pusher(pusher_app_id, pusher_key, pusher_secret)
        return True
    except:
        return False


def get_google_creds(config=None):
    if config is None:
        config = app.config

    user = config.get('GOOGLE_ACCOUNT_USER', None)
    password = config.get('GOOGLE_ACCOUNT_PASS', None)
    return user, password
