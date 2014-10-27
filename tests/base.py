from unittest import TestCase
from mock import patch, Mock

from functools import wraps


class KitTestCase(TestCase):
    def start_patch(self, tool):
        #  Patch all requests to twilio_numbers()
        self.twilio_numbers_patcher = patch('rapid_response_kit.tools.{}.twilio_numbers'.format(tool))
        self.twilio_numbers_patch = self.twilio_numbers_patcher.start()
        self.twilio_numbers_patch.return_value = []

        #  Patch all requests to twilio()
        self.twilio_patcher = patch('rapid_response_kit.tools.{}.twilio'.format(tool))
        self.twilio_patch = self.twilio_patcher.start()
        self.patchio = Mock()
        self.twilio_patch.return_value = self.patchio

    def stop_patch(self):
        self.twilio_numbers_patcher.stop()
        self.twilio_patcher.stop()
