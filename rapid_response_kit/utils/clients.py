from flask import current_app as app
from parse_rest.connection import register
from twilio.rest import TwilioRestClient
from pusher import Pusher


def twilio():
    return TwilioRestClient(app.config['TWILIO_ACCOUNT_SID'],
                            app.config['TWILIO_AUTH_TOKEN'])


def parse_connect(config=None):
    if config is None:
        config = app.config

    app_id = config.get('PARSE_APP_ID', None)
    rest_key = config.get('PARSE_REST_KEY', None)

    if not (app_id and rest_key):
        return False

    try:
        register(app_id, rest_key)
        return True
    except:
        return False


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
