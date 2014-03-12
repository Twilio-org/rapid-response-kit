from mock import call
from nose.tools import assert_equal
from rapid_response_kit.app import app
from tests.base import KitTestCase


class TownHallTestCase(KitTestCase):

    def setUp(self):
        self.app = app.test_client()
        self.start_patch('town_hall')

    def tearDown(self):
        self.stop_patch()

    def test_get(self):
        response = self.app.get('/town-hall')
        assert_equal(response.status_code, 200)

    def test_post(self):
        self.app.post('/town-hall', data={'numbers': '4158675309\n4158675310',
                                          'twilio_number': '1415TWILIO'})

        join_url = 'http://twimlets.com/echo?Twiml=%3CResponse%3E%3CDial%3E%3CConference%3Etown-hall%3C%2FConference%3E%3C%2FDial%3E%3C%2FResponse%3E'

        self.patchio.calls.create.assert_has_calls([
            call(
                url=join_url,
                to='+14158675309',
                from_='1415TWILIO'
            ),
            call(
                url=join_url,
                to='+14158675310',
                from_='1415TWILIO'
            )
        ])

