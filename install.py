from clint.textui import colored
import os

print
print
print colored.red(" --- Enter your Twilio information below to complete install --- ")
print
print

account_sid = raw_input('Twilio Account Sid: ')
auth_token = raw_input('Twilio Auth Token: ')

print
print
print colored.red(" --- Enter your Parse information below to use Optional Survey app --- ")
print
print

parse_app_id = raw_input('Parse APP ID: ')
parse_rest_key = raw_input('Parse Rest Key: ')

config = """# Configuration Auto-generated during installation
SECRET_KEY = {}
TWILIO_ACCOUNT_SID = '{}'
TWILIO_AUTH_TOKEN = '{}'
PARSE_APP_ID = '{}'
PARSE_REST_KEY = '{}'""".format(repr(os.urandom(20)), account_sid, auth_token,parse_app_id,parse_rest_key)


f = open('rapid_response_kit/utils/config.py', 'w')
f.write(config)
f.close()