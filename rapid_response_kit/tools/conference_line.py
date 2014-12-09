from rapid_response_kit.utils.compat import urlencode

from rapid_response_kit.utils.clients import twilio
from rapid_response_kit.utils.helpers import (
    twilio_numbers,
    parse_numbers,
    fallback
)

from flask import render_template, request, redirect, flash

from twilio.twiml import Response


def install(app):
    app.config.apps.register('conference-line', 'Conference Line',
                             '/conference-line')

    @app.route('/conference-line', methods=['GET'])
    def show_conference_line():
        numbers = twilio_numbers()
        return render_template("conference-line.html", numbers=numbers)

    @app.route('/conference-line', methods=['POST'])
    def do_conference_line():
        whitelist = parse_numbers(request.form.get('whitelist', ''))
        room = request.form.get('room', '')

        data = {}

        if len(whitelist):
            data['whitelist'] = whitelist

        if len(room):
            data['room'] = room

        qs = urlencode(data, True)
        url = "{}/handle?{}".format(request.base_url, qs)

        try:
            client = twilio()
            client.phone_numbers.update(
                request.form['twilio_number'],
                friendly_name='[RRKit] Conference Line',
                voice_url=url,
                voice_method='GET',
                fallback_voice_url=fallback(),
                fallback_voice_method='GET'
            )

            flash('Conference Line configured', 'success')
        except Exception:
            flash('Error configuring number', 'danger')

        return redirect('/conference-line')

    @app.route('/conference-line/handle')
    def handle_conference_line():
        whitelist = request.args.getlist('whitelist')

        if len(whitelist) > 0:
            if request.args['From'] not in whitelist:
                resp = Response()
                resp.say('Sorry, you are not authorized to call this number')
                return str(resp)

        room = request.args.get('room', False)

        if room:
            resp = Response()
            with resp.dial() as d:
                d.conference(room)
            return str(resp)

        # Gather the room code
        resp = Response()
        with resp.gather(numDigits=3, action='/conference-line/connect',
                         method='GET') as g:
            g.say("Enter a 3-digit room code")

        return str(resp)

    @app.route('/conference-line/connect')
    def connect_conference_line():
        resp = Response()
        with resp.dial() as d:
            d.conference(request.args['Digits'])
        return str(resp)
