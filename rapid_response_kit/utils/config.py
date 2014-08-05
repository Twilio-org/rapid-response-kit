SECRET_KEY = ''
TWILIO_ACCOUNT_SID = ''
TWILIO_AUTH_TOKEN = ''

try: 
   import local_config
except:
  import os
  SECRET_KEY = os.environ['SECRET_KEY']
  TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
  TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
