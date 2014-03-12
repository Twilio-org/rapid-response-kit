from clint.textui import colored
import os

print
print
print colored.red(" --- Enter your Twilio information below to complete install --- ")
print
print

account_sid = raw_input('Twilio Account Sid: ')
auth_token = raw_input('Twilio Auth Token: ')

config = """# Configuration Auto-generated during installation
SECRET_KEY = {}
TWILIO_ACCOUNT_SID = '{}'
TWILIO_AUTH_TOKEN = '{}'""".format(repr(os.urandom(20)), account_sid, auth_token)

f = open('rapid_response_kit/utils/config.py', 'w')
f.write(config)
f.close()