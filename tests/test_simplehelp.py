from nose.tools import assert_equal
from rapid_response_kit.app import app
from tests.base import KitTestCase


class SimpleHelpTestCase(KitTestCase):

    def setUp(self):
        self.app = app.test_client()
        self.start_patch('simplehelp')

    def tearDown(self):
        self.stop_patch()

    def test_get(self):
        response = self.app.get('/simplehelp')
        assert_equal(response.status_code, 200)

    def test_post(self):
        self.app.post('/simplehelp', data={'menu_name': 'Tommy Tutone',
                                           'type_1': 'Call',
                                           'desc_1': 'Call Jenny',
                                           'value_1': '4158675309',
                                           'type_2': 'Info',
                                           'desc_2': 'Lost and Found',
                                           'value_2': 'I got your number',
                                           'twilio_number': 'PNSid'})

        expected_voice_url = 'http://localhost/simplehelp/handle?name=Tommy+Tutone&opt_1=Call%3ACall+Jenny%3A4158675309&opt_2=Info%3ALost+and+Found%3AI+got+your+number'
        expected_fallback_url = 'http://twimlets.com/echo?Twiml=%3C%3Fxml+version%3D%221.0%22+encoding%3D%22UTF-8%22%3F%3E%3CResponse%3E%3CSay%3ESystem+is+down+for+maintenance%3C%2FSay%3E%3C%2FResponse%3E'

        self.patchio.phone_numbers.update.assert_called_with(
            'PNSid',
            voice_url=expected_voice_url,
            voice_fallback_method='GET',
            friendly_name='[RRKit] Simple Help Line',
            voice_method='GET',
            voice_fallback_url=expected_fallback_url)

    def test_handle(self):
        response = self.app.get('/simplehelp/handle?name=Tommy+Tutone&opt_1=Call%3ACall+Jenny%3A4158675309&opt_2=Info%3ALost+and+Found%3AI+got+your+number')
        assert 'Thank you for calling Tommy Tutone' in response.data
        assert 'Call Jenny, press 1' in response.data
        assert 'Lost and Found, press 2' in response.data

    def test_handle_call(self):
        response = self.app.post('/simplehelp/handle?name=Tommy+Tutone&opt_1=Call%3ACall+Jenny%3A4158675309&opt_2=Info%3ALost+and+Found%3AI+got+your+number', data={'Digits': '1'})
        assert '<Dial>4158675309</Dial>' in response.data

    def test_handle_info(self):
        response = self.app.post('/simplehelp/handle?name=Tommy+Tutone&opt_1=Call%3ACall+Jenny%3A4158675309&opt_2=Info%3ALost+and+Found%3AI+got+your+number', data={'Digits': '2'})
        assert 'I got your number' in response.data

    def test_handle_invalid(self):
        response = self.app.post('/simplehelp/handle?name=Tommy+Tutone&opt_1=Call%3ACall+Jenny%3A4158675309&opt_2=Info%3ALost+and+Found%3AI+got+your+number', data={'Digits': '3'})
        assert "Sorry, that's not a valid choice" in response.data
