from rapid_response_kit.utils.clients import twilio, pusher_connect
from clint.textui import colored

from twilio.twiml import Response

from pusher import Pusher

from flask import render_template, request, flash, redirect
from rapid_response_kit.utils.helpers import (
    parse_numbers,
    echo_twimlet,
    twilio_numbers)


def install(app):
    if pusher_connect(app.config):
        app.config.apps.register('noticeboard', 'Noticeboard', '/noticeboard')
    else:
        print colored.red(
            'Noticeboard requires Pusher, please add PUSHER_APP_ID, PUSHER_KEY and PUSHER_SECRET to your config.py')
        return

    @app.route('/noticeboard', methods=['GET'])
    def show_noticeboard():
        numbers = twilio_numbers('phone_number')
        return render_template("noticeboard.html", url=request.base_url + '/live', numbers=numbers)


    @app.route('/noticeboard', methods=['POST'])
    def do_noticeboard():

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
        r.message('Thank you, your image has been posted to ' + request.url_root + 'noticeboard/live')
        return str(r)

    @app.route('/noticeboard/live', methods=['GET'])
    def show_noticeboard_live():
        pusher_key = app.config.get('PUSHER_KEY', '')
        return render_template('noticeboard_live.html', pusher_key=pusher_key)
