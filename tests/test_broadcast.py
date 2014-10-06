from mock import patch, Mock, call
from nose.tools import assert_equal
from rapid_response_kit.app import app
from tests.base import KitTestCase


class BroadcastTestCase(KitTestCase):

    def setUp(self):
        self.app = app.test_client()
        self.start_patch('broadcast')

    def tearDown(self):
        self.stop_patch()

    def test_get(self):
        response = self.app.get('/broadcast')
        assert_equal(response.status_code, 200)

    def test_post_sms(self):
        self.app.post('/broadcast', data={'method': 'sms',
                                          'twilio_number': '1415TWILIO',
                                          'numbers': '14158675309',
                                          'message': 'Test Broadcast'})

        self.patchio.messages.create.assert_called_with(
            body='Test Broadcast',
            to='+14158675309',
            from_='1415TWILIO',
            media_url=None
        )

    def test_post_sms_multi(self):
        self.app.post('/broadcast', data={'method': 'sms',
                                          'twilio_number': '1415TWILIO',
                                          'numbers': '14158675309\n14158675310',
                                          'message': 'Test Broadcast'})

        self.patchio.messages.create.assert_has_calls([
            call(
                body='Test Broadcast',
                to='+14158675309',
                from_='1415TWILIO',
                media_url=None
            ),
            call(
                body='Test Broadcast',
                to='+14158675310',
                from_='1415TWILIO',
                media_url=None
            ),
        ])

    def test_post_mms(self):
        """ Identical to above, but with a media URL"""

        self.app.post('/broadcast', data={'method': 'sms',
                                          'twilio_number': '1415TWILIO',
                                          'numbers': '14158675309',
                                          'message': 'Test Broadcast',
                                          'media': 'http://i.imgur.com/UMlp0iK.jpg'})

        self.patchio.messages.create.assert_called_with(
            body='Test Broadcast',
            to='+14158675309',
            from_='1415TWILIO',
            media_url='http://i.imgur.com/UMlp0iK.jpg'
        )

    def test_post_multi_mms(self):
        self.app.post('/broadcast', data={'method': 'sms',
                                          'twilio_number': '1415TWILIO',
                                          'numbers': '14158675309\n14158675310',
                                          'message': 'Test Broadcast',
                                          'media': 'http://i.imgur.com/UMlp0iK.jpg'})

        self.patchio.messages.create.assert_has_calls([
            call(
                body='Test Broadcast',
                to='+14158675309',
                from_='1415TWILIO',
                media_url='http://i.imgur.com/UMlp0iK.jpg'
            ),
            call(
                body='Test Broadcast',
                to='+14158675310',
                from_='1415TWILIO',
                media_url='http://i.imgur.com/UMlp0iK.jpg'
            ),
        ])

    def test_post_call(self):
        self.app.post('/broadcast', data={'method': 'voice',
                                          'twilio_number': '1415TWILIO',
                                          'numbers': '14158675309',
                                          'message': 'Test Broadcast'})

        self.patchio.calls.create.assert_called_with(
            url='http://twimlets.com/echo?Twiml=%3CResponse%3E%3CSay%3ETest+Broadcast%3C%2FSay%3E%3C%2FResponse%3E',
            to='+14158675309',
            from_='1415TWILIO')

    def test_post_call_multi(self):
        self.app.post('/broadcast', data={'method': 'voice',
                                          'twilio_number': '1415TWILIO',
                                          'numbers': '14158675309\n14158675310',
                                          'message': 'Test Broadcast'})

        self.patchio.calls.create.assert_has_calls([
            call(
                url='http://twimlets.com/echo?Twiml=%3CResponse%3E%3CSay%3ETest+Broadcast%3C%2FSay%3E%3C%2FResponse%3E',
                to='+14158675309',
                from_='1415TWILIO'
            ),
            call(
                url='http://twimlets.com/echo?Twiml=%3CResponse%3E%3CSay%3ETest+Broadcast%3C%2FSay%3E%3C%2FResponse%3E',
                to='+14158675310',
                from_='1415TWILIO'
            ),
        ])



