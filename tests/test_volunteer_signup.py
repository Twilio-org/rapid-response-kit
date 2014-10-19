from mock import call
from nose.tools import assert_equal
from rapid_response_kit.app import app
from tests.base import KitTestCase


class VolunteerSignupTestCase(KitTestCase):

    def setUp(self):
        app.config['GOOGLE_ACCOUNT_USER'] = 'email@test.com'
        app.config['GOOGLE_ACCOUNT_PASS'] = 'password'
        self.app = app.test_client()
        self.start_patch('volunteer_signup')

    def tearDown(self):
        self.stop_patch()

    def test_get(self):
        response = self.app.get('/volunteer-signup')
        self.assertEqual(response.status_code, 200)


    def test_post_sms_send(self):
        self.app.post('/volunteer-signup', data={'numbers': '4158675309',
                                          'twilio_number': 'PNSid',
                                          'message': 'Test Volunteer Signup'})

        self.patchio.messages.create.assert_called(
            to='+14158675309'
        )

    def test_post_number_update(self):
        self.app.post('/volunteer-signup', data={
                                          'twilio_number': 'PNSid'})
        expected_voice_url = 'http://localhost/volunteer-signup/handle?'
        expected_fallback_url = 'http://twimlets.com/echo?Twiml=%3CResponse%3E%3CSay%3ESystem+is+down+for+maintenance%3C%2FSay%3E%3C%2FResponse%3E'

        self.patchio.phone_numbers.update.assert_called(
            'PNSid',
            sms_url=expected_voice_url,
            sms_fallback_method='GET',
            friendly_name='[RRKit] Volunteer Signup',
            sms_method='POST',
            sms_fallback_url=expected_fallback_url)


    def test_handle(self):
        self.app.post('/volunteer-signup/handle', data={
                                          'From': '4158675309',
                                          'Body': 'Reply to volunteer'})

        self.patchio.messages.create.assert_called(
            to='+14158675309'
        )
