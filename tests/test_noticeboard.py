from mock import call
from nose.tools import assert_equal
from rapid_response_kit.app import app
from tests.base import KitTestCase


class NoticeboardTestCase(KitTestCase):

    def setUp(self):
        self.app = app.test_client()

        self.start_patch('noticeboard')

    def tearDown(self):
        self.stop_patch()


    def test_post_sms_send(self):
        response = self.app.post('/noticeboard', data={
                                          'twilio_number': '1415TWILIO',
                                          'numbers': '14158675309',
                                          'message': 'Test Noticeboard'})


        self.patchio.messages.create.assert_called_with(
            body='Test Noticeboard',
            to='+14158675309',
            from_='1415TWILIO',
            media_url=None
        )

    def test_post_mms(self):
        """ Identical to above, but with a media URL"""

        self.app.post('/noticeboard', data={
                                          'twilio_number': '1415TWILIO',
                                          'numbers': '14158675309',
                                          'message': 'Test Noticeboard',
                                          'media': 'http://i.imgur.com/UMlp0iK.jpg'})

        self.patchio.messages.create.assert_called_with(
            body='Test Noticeboard',
            to='+14158675309',
            from_='1415TWILIO',
            media_url='http://i.imgur.com/UMlp0iK.jpg'
        )

    def test_noticeboard_inbound_no_creds(self):
        response = self.app.post('/noticeboard/post')
        assert_equal(response.status_code, 200)
