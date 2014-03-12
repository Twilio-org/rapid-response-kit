from nose.tools import assert_equal
from rapid_response_kit.app import app
from tests.base import KitTestCase


class AutorespondTestCase(KitTestCase):

    def setUp(self):
        self.app = app.test_client()
        self.start_patch('autorespond')

    def tearDown(self):
        self.stop_patch()

    def test_get(self):
        response = self.app.get('/auto-respond')
        assert_equal(response.status_code, 200)

    def test_post_invalid(self):
        response = self.app.post('/auto-respond', data={},
                                 follow_redirects=True)
        assert 'Please provide a message' in response.data

    def test_post_valid_sms(self):
        self.app.post('/auto-respond', data={'sms-message': 'Test Message',
                                             'twilio_number': 'PNSid'})

        expected_url = 'http://twimlets.com/echo?Twiml=%3CResponse%3E%3CSms%3ETest+Message%3C%2FSms%3E%3C%2FResponse%3E'

        self.patchio.phone_numbers.update.assert_called_with(
            'PNSid',
            friendly_name='[RRKit] Auto-Respond',
            voice_url='',
            voice_method='GET',
            sms_method='GET',
            sms_url=expected_url)

    def test_post_valid_voice(self):
        self.app.post('/auto-respond', data={'voice-message': 'Test Message',
                                             'twilio_number': 'PNSid'})

        expected_url = 'http://twimlets.com/echo?Twiml=%3CResponse%3E%3CSay%3ETest+Message%3C%2FSay%3E%3C%2FResponse%3E'

        self.patchio.phone_numbers.update.assert_called_with(
            'PNSid',
            friendly_name='[RRKit] Auto-Respond',
            voice_url=expected_url,
            voice_method='GET',
            sms_method='GET',
            sms_url='')



