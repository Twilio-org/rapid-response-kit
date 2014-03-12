from nose.tools import assert_equal
from rapid_response_kit.app import app
from tests.base import KitTestCase


class ForwardTestCase(KitTestCase):

    def setUp(self):
        self.app = app.test_client()
        self.start_patch('forward')

    def tearDown(self):
        self.stop_patch()

    def test_get(self):
        response = self.app.get('/forwarder')
        assert_equal(response.status_code, 200)

    def test_post(self):
        self.app.post('/forwarder', data={'number': '4158675309',
                                          'twilio_number': 'PNSid'})

        expected_url = 'http://twimlets.com/echo?Twiml=%3CResponse%3E%3CDial%3E%2B14158675309%3C%2FDial%3E%3C%2FResponse%3E'

        self.patchio.phone_numbers.update.assert_called_with(
            'PNSid',
            voice_url=expected_url,
            friendly_name='[RRKit] Forwarder',
            voice_method='GET')