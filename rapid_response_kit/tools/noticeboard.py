from rapid_response_kit.utils.clients import twilio, pusher_connect
from rapid_response_kit.utils.helpers import (
    parse_numbers,
    echo_twimlet,
    twilio_numbers)

from clint.textui import colored

from twilio.twiml import Response

from pusher import Pusher

from flask import render_template, request, flash, redirect


def install(app):
    if pusher_connect(app.config):
        app.config.apps.register('noticeboard', 'Noticeboard', '/noticeboard')
    else:
        print colored.red(
            '''
            Noticeboard requires Pusher, please add PUSHER_APP_ID, PUSHER_KEY
            and PUSHER_SECRET to your config.py''')
        return

    @app.route('/noticeboard', methods=['GET'])
    def show_noticeboard():
        numbers = twilio_numbers()
        return render_template(
            "noticeboard.html",
            url='{0}/live'.format(request.base_url),
            numbers=numbers
        )


    @app.route('/noticeboard', methods=['POST'])
    def do_noticeboard():
        numbers = parse_numbers(request.form['numbers'])

        url = "{0}noticeboard/post".format(request.url_root)

        client = twilio()

        client.phone_numbers.update(request.form['twilio_number'],
                                    sms_url=url,
                                    sms_method='POST',
                                    friendly_name='[RRKit] Noticeboard')

        from_number = client.phone_numbers.get(request.form['twilio_number'])

        for num in numbers:
            try:
                client.messages.create(
                    to=num,
                    from_=from_number.phone_number,
                    body=request.form.get('message', ''),
                    media_url=request.form.get('media', None)
                )
                flash('Sent {0} the message'.format(num), 'success')
            except:
                flash('Failed to send {0} the message'.format(num), 'danger')
                return redirect('/noticeboard')

        return redirect('/noticeboard')

    @app.route('/noticeboard/post', methods=['POST'])
    def handle_noticeboard_inbound():

        pusher_key = app.config.get('PUSHER_KEY', None)
        pusher_secret = app.config.get('PUSHER_SECRET', None)
        pusher_app_id = app.config.get('PUSHER_APP_ID', None)

        p = Pusher(pusher_app_id, pusher_key, pusher_secret)

        p['rrk_noticeboard_live'].trigger(
        'new_message',
            {
                'image': request.values.get('MediaUrl0', None),
                'body': request.values.get('Body', None),
                'from': request.values.get('From', None)
            }
        )

        r = Response()
        r.message(
            '''Thank you, your image has been posted
            to {0}noticeboard/live'''.format(request.url_root))
        return r.toxml()

    @app.route('/noticeboard/live', methods=['GET'])
    def show_noticeboard_live():
        pusher_key = app.config.get('PUSHER_KEY', '')
        return render_template(
            'noticeboard_live.html',
            pusher_key=pusher_key
        )
