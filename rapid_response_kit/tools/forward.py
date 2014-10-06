from flask import render_template, request, redirect, flash

from rapid_response_kit.utils.clients import twilio
from rapid_response_kit.utils.helpers import (
    echo_twimlet,
    convert_to_e164,
    twilio_numbers
)


def install(app):
    app.config.apps.register('forwarder', 'Forwarder', '/forwarder')

    @app.route('/forwarder', methods=['GET'])
    def show_forwarder():
        numbers = twilio_numbers()
        return render_template("forwarder.html", numbers=numbers)

    @app.route('/forwarder', methods=['POST'])
    def do_forwarder():
        normalized = convert_to_e164(request.form.get('number', ''))

        if not normalized:
            flash('Phone number is invalid, please try again', 'danger')
            return redirect('/forwarder')

        twiml = '<Response><Dial>{}</Dial></Response>'.format(normalized)
        url = echo_twimlet(twiml)

        try:
            client = twilio()
            client.phone_numbers.update(request.form['twilio_number'],
                                        friendly_name='[RRKit] Forwarder',
                                        voice_url=url,
                                        voice_method='GET')

            flash('Number configured', 'success')
        except Exception:
            flash('Error configuring number', 'danger')

        return redirect('/forwarder')
