from mock import call
from nose.tools import assert_equal
from rapid_response_kit.app import app
from tests.base import KitTestCase


class VolunteerSignupTestCase(KitTestCase):

    def setUp(self):
        self.app = app.test_client()
        self.start_patch('volunteer_signup')

    def tearDown(self):
        self.stop_patch()

    def test_get(self):
        response = self.app.get('/volunteer-signup')
        assert_equal(response.status_code, 200)

    def test_post(self):
        self.app.post('/volunteer-signup', data={'numbers': '4158675309',
                                          'twilio_number': 'PNSid',
                                          'message': 'Test Volunteer Signup'})

        self.patchio.messages.create.assert_called(
            to='+14158675309'
            )
