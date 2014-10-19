try:
   import local_config
except:
    try:
      import os
      SECRET_KEY = os.environ['SECRET_KEY']
      TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
      TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
      GOOGLE_ACCOUNT_USER = os.environ['GOOGLE_ACCOUNT_USER']
      GOOGLE_ACCOUNT_PASS = os.environ['GOOGLE_ACCOUNT_PASS']
      PUSHER_APP_ID = os.environ['PUSHER_APP_ID']
      PUSHER_KEY = os.environ['PUSHER_KEY']
      PUSHER_SECRET = os.environ['PUSHER_SECRET']
      PARSE_APP_ID = os.environ['Application ID']
      PARSE_REST_KEY = os.environ['REST API key']
    except:
        pass
