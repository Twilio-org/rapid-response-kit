from .compat import urlencode, urlunparse, urlparse

from rapid_response_kit.utils.clients import twilio
import phonenumbers


def parse_numbers(raw):
    numbers = raw.split("\n")
    result = []
    for number in numbers:
        converted = convert_to_e164(number)
        if converted and converted not in result:
            result.append(converted)

    return result


def convert_to_e164(raw_phone):
    if not raw_phone:
        return

    if raw_phone[0] == '+':
        # Phone number may already be in E.164 format.
        parse_type = None
    else:
        # If no country code information present, assume it's a US number
        parse_type = "US"

    try:
        phone_representation = phonenumbers.parse(raw_phone, parse_type)
    except phonenumbers.NumberParseException:
        return None

    return phonenumbers.format_number(phone_representation,
                                      phonenumbers.PhoneNumberFormat.E164)


def check_is_valid_url(url):
    o = urlparse(url)
    if o.scheme in ['https', 'http']:
        return o.geturl()
    return None


def echo_twimlet(twiml):
    params = {'Twiml': twiml}
    qs = urlencode(params)
    return urlunparse(('http', 'twimlets.com', 'echo', '', qs, ''))


def fallback(message='Sorry the service is down for maintenance'):
    twiml = '<Response><Say>{}</Say></Response>'.format(message)
    return echo_twimlet(twiml)


def twilio_numbers(id_field='sid'):
    client = twilio()

    numbers = client.phone_numbers.list()

    result = []
    for number in numbers:
        if number.friendly_name.startswith('[RRKit]'):
            display_name = '[{}] {}'.format(
                number.friendly_name[len('[RRKit]') + 1:],
                number.phone_number
            )
        else:
            display_name = number.phone_number

        result.append((getattr(number, id_field), display_name))

    return result
