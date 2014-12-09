from mock import call
from nose.tools import assert_equal
from rapid_response_kit.app import app
from tests.base import KitTestCase


class SurveyTestCase(KitTestCase):

    def setUp(self):
        app.config['PARSE_APP_ID'] = 'ApplicationID'
        app.config['PARSE_REST_KEY'] = 'REST API key'
        self.app = app.test_client()
        self.start_patch('survey')

    def tearDown(self):
        self.stop_patch()

    def test_post_sms(self):
        self.app.post('/survey', data=
          {
            'twilio_number': '1415TWILIO',
            'numbers': '14158675309',
            'message': 'Test Survey'
          })

        self.patchio.phone_numbers.update.assert_called(
            '1415TWILIO',
            friendly_name='[RRKit] Survey',
            )

        self.patchio.messages.create.assert_called(
            body='Test Survey',
            to='+14158675309',
            from_='1415TWILIO',
            media_url=None
        )

    def test_post_sms_multi(self):
        self.app.post('/survey', data=
          {
            'twilio_number': '1415TWILIO',
            'numbers': '14158675309\n14158675310',
            'message': 'Test Survey'
          })

        self.patchio.messages.create.assert_called([
            call(
                body='Test Survey',
                to='+14158675309',
                from_='1415TWILIO',
                media_url=None
            ),
            call(
                body='Test Survey',
                to='+14158675310',
                from_='1415TWILIO',
                media_url=None
            ),
        ])
