from rapid_response_kit.utils.clients import twilio, pusher_connect
from rapid_response_kit.utils.helpers import (
    parse_numbers,
    echo_twimlet,
    twilio_numbers,
    check_is_valid_url
)

from clint.textui import colored
from twilio.twiml import Response
from pusher import Pusher
from flask import render_template, request, flash, redirect


def install(app):
    if pusher_connect(app.config):
        app.config.apps.register('noticeboard', 'Noticeboard', '/noticeboard')
    else:
        print(colored.red(
                    '''
                    Noticeboard requires Pusher credentials.
                    Please add PUSHER_APP_ID, PUSHER_KEY and PUSHER_SECRET
                    to rapid_response_kit/utils/config.py'''))
        return

    @app.route('/noticeboard', methods=['GET'])
    def show_noticeboard():
        numbers = twilio_numbers()
        client = twilio()

        # Build a list of numbers that are being used for Noticeboard
        noticeboard_numbers = []
        for p in client.phone_numbers.list():
            if '[RRKit] Noticeboard' in p.friendly_name:
                noticeboard_numbers.append(p.phone_number)

        return render_template(
            "noticeboard.html",
            url='{0}/live'.format(request.base_url),
            numbers=numbers,
            noticeboards=noticeboard_numbers
        )

    @app.route('/noticeboard', methods=['POST'])
    def do_noticeboard():
        client = twilio()

        url = "{0}noticeboard/post".format(request.url_root)
        client.phone_numbers.update(request.form['twilio_number'],
                                    sms_url=url,
                                    sms_method='POST',
                                    friendly_name='[RRKit] Noticeboard')

        from_number = client.phone_numbers.get(request.form['twilio_number'])

        live_url = '{0}noticeboard/live/{1}'.format(
            request.url_root,
            from_number.phone_number
        )
        numbers = parse_numbers(request.form['numbers'])
        body = request.form.get('message', '').replace('{URL}', live_url)
        media = check_is_valid_url(request.form.get('media', ''))

        for num in numbers:
            client.messages.create(
                to=num,
                from_=from_number.phone_number,
                body=body,
                media_url=media
            )
            flash('Sent {0} the message'.format(num), 'success')


        return redirect('/noticeboard')

    @app.route('/noticeboard/post', methods=['POST'])
    def handle_noticeboard_inbound():

        pusher_key = app.config.get('PUSHER_KEY', None)
        pusher_secret = app.config.get('PUSHER_SECRET', None)
        pusher_app_id = app.config.get('PUSHER_APP_ID', None)

        try:
            p = Pusher(pusher_app_id, pusher_key, pusher_secret)

            p['rrk_noticeboard_live'].trigger(
                'new_message',
                {
                    'image': request.values.get('MediaUrl0', None),
                    'body': request.values.get('Body', None),
                    'from': request.values.get('From', None)
                }
            )
        except:
            return '<Response />'

        to = request.values.get('To', '')
        r = Response()
        r.message(
            '''Thank you, your image has been posted
            to {0}noticeboard/live/{1}'''.format(request.url_root, to))
        return r.toxml()

    @app.route('/noticeboard/live/<number>', methods=['GET'])
    def show_noticeboard_live(number=None):
        pusher_key = app.config.get('PUSHER_KEY', '')
        twilio_client = twilio()
        try:
            cleaned_number = number
        except:
            flash('We did not receive a correct number', 'danger')
            return redirect('/noticeboard')

        # Build a list of messages to our number that has media attached
        msgs = []
        for m in twilio_client.messages.list(to=cleaned_number):
            if int(m.num_media) > 0:
                msgs.append(m)

        '''
        Super janky because media is seperate from message resources.

        Let's mash the bits we want together and then add them to a list
        - Paul Hallett
        '''
        msg_media_list = []
        for m in msgs:
            d = {}
            d['image_url'] = twilio_client.media(m.sid).list()[0].uri
            d['body'] = m.body
            d['from'] = m.from_
            msg_media_list.append(d)

        return render_template(
            'noticeboard_live.html',
            pusher_key=pusher_key,
            messages=msg_media_list,
            number=number
        )
