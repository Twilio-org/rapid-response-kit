from rapid_response_kit.utils.compat import urlencode

from flask import render_template, request, redirect, flash

from rapid_response_kit.utils.clients import twilio
from rapid_response_kit.utils.helpers import (
    parse_numbers,
    echo_twimlet,
    twilio_numbers
)

from twilio.twiml import Response


def install(app):
    app.config.apps.register('ringdown', 'Ringdown', '/ringdown')

    @app.route('/ringdown', methods=['GET'])
    def show_ringdown():
        numbers = twilio_numbers()
        return render_template("ringdown.html", numbers=numbers)

    @app.route('/ringdown', methods=['POST'])
    def do_ringdown():
        numbers = parse_numbers(request.form.get('numbers', ''))
        data = {
            'stack': numbers,
            'sorry': request.form.get('sorry', '')
        }

        url = "{}/handle?{}".format(request.base_url, urlencode(data, True))

        r = Response()
        r.say('System is down for maintenance')
        fallback_url = echo_twimlet(r.toxml())

        try:
            client = twilio()
            client.phone_numbers.update(request.form['twilio_number'],
                                        friendly_name='[RRKit] Ringdown',
                                        voice_url=url,
                                        voice_method='GET',
                                        voice_fallback_url=fallback_url,
                                        voice_fallback_method='GET')

            flash('Number configured', 'success')
        except Exception:
            flash('Error configuring number', 'danger')

        return redirect('/ringdown')

    @app.route('/ringdown/handle')
    def handle_ringdown():
        stack = request.args.getlist('stack')
        sorry = request.args.get('sorry', 'Sorry, no one answered')

        if len(stack) == 0:
            # Nothing else to ringdown
            resp = Response()
            resp.say(sorry)

            return str(resp)

        top = stack.pop(0)

        data = {
            'stack': stack,
            'sorry': sorry
        }

        qs = urlencode(data, True)

        resp = Response()
        resp.dial(top, timeout=10, action="/ringdown/handle?{}".format(qs),
                  method='GET')

        return str(resp)
