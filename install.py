from clint.textui import colored
import os

print
print
print colored.red(" --- Enter your Twilio information below to complete install --- ")
print
print

account_sid = raw_input('Twilio Account Sid: ')
auth_token = raw_input('Twilio Auth Token: ')

config = """\n\n# Configuration Auto-generated during installation
SECRET_KEY = {}
TWILIO_ACCOUNT_SID = '{}'
TWILIO_AUTH_TOKEN = '{}'""".format(repr(os.urandom(20)), account_sid, auth_token)

f = open('rapid_response_kit/utils/config.py', 'rw')
contents = f.read()
f.close()
f = open('rapid_response_kit/utils/config.py', 'w')
f.write(contents + config)
f.close()

print
print
print colored.red(" --- Would you like to add other credentials now? ---")
print
print

decision = raw_input("Type 'yes' or 'no': ")

if decision == 'yes':
    firebase_url = raw_input('Firebase Url (optional): ')
    firebase_secret = raw_input('Firebase Secret Key (optional): ')
    pusher_app_id = raw_input('Pusher App ID (optional): ')
    pusher_key = raw_input('Pusher Key (optional): ')
    pusher_secret = raw_input('Pusher Secret (optional): ')
    google_user = raw_input('Google email (optional): ')
    google_pass = raw_input('Google password (optional): ')

    new_config = '''
GOOGLE_ACCOUNT_USER = '{}'
GOOGLE_ACCOUNT_PASS = '{}'
PUSHER_APP_ID = '{}'
PUSHER_KEY = '{}'
PUSHER_SECRET = '{}'
FIREBASE_URL = '{}'
FIREBASE_SECRET = '{}'
    '''.format(
        google_user,
        google_pass,
        pusher_app_id,
        pusher_key,
        pusher_secret,
        firebase_url,
        firebase_secret)

    f = open('rapid_response_kit/utils/config.py', 'rw')
    contents = f.read()
    f.close()
    f = open('rapid_response_kit/utils/config.py', 'w')
    f.write(contents + new_config)
    f.close()
