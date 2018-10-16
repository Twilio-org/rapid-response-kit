from rapid_response_kit.utils.compat import urlencode

from flask import render_template, request, redirect, flash

from rapid_response_kit.utils.clients import twilio
from rapid_response_kit.utils.helpers import (
    parse_numbers,
    twilio_numbers,
)

from twilio.twiml import Response


def install(app):
    app.config.apps.register('sms-forwarder', 'SMS Forwarder',
                             '/sms-forwarder')

    @app.route('/sms-forwarder', methods=['GET'])
    def show_sms_forwarder():
        numbers = twilio_numbers()
        return render_template("sms-forwarder.html", numbers=numbers)

    @app.route('/sms-forwarder', methods=['POST'])
    def do_sms_forwarder():
        numbers = parse_numbers(request.form.get('numbers', ''))
        data = {
            'recipients': numbers,
        }

        url = "{}/handle?{}".format(request.base_url, urlencode(data, True))

        try:
            client = twilio()
            client.phone_numbers.update(request.form['twilio_number'],
                                        friendly_name='[RRKit] SMS Forwarder',
                                        sms_url=url,
                                        sms_method='GET')
            flash('Number configured', 'success')
        except Exception:
            flash('Error configuring number', 'danger')

        return redirect('/sms-forwarder')

    @app.route('/sms-forwarder/handle')
    def handle_sms_forwarder():
        recipients = request.args.getlist('recipients')
        sender = request.args.get('From')
        original_message = request.args.get('Body')

        message = 'From {}:\n{}'.format(sender, original_message)

        resp = Response()

        for r in recipients:
            resp.message(message, to=r)

        return str(resp)
