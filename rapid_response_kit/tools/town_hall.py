from rapid_response_kit.utils.clients import twilio
from flask import render_template, request, redirect, flash
from rapid_response_kit.utils.helpers import (
    parse_numbers,
    echo_twimlet,
    twilio_numbers
)


def install(app):
    app.config.apps.register('town-hall', 'Town Hall', '/town-hall')

    @app.route('/town-hall', methods=['GET'])
    def show_town_hall():
        numbers = twilio_numbers('phone_number')
        return render_template("town-hall.html", numbers=numbers)

    @app.route('/town-hall', methods=['POST'])
    def do_town_hall():
        numbers = parse_numbers(request.form.get('numbers', ''))
        twiml = '<Response><Dial><Conference>{}</Conference></Dial></Response>'
        room = request.form.get('room', 'town-hall')
        url = echo_twimlet(twiml.format(room))

        client = twilio()

        for number in numbers:
            try:
                client.calls.create(
                    url=url,
                    to=number,
                    from_=request.form['twilio_number']
                )
                flash(
                    '{} contacted to join {}'.format(number, room), 'success')
            except Exception:
                flash('Unable to contact {}'.format(number))

        return redirect('/town-hall')
