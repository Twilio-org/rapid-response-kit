from rapid_response_kit.utils.compat import urlencode

from rapid_response_kit.utils.clients import twilio
from flask import render_template, request, redirect, flash
from rapid_response_kit.utils.helpers import echo_twimlet
from twilio.twiml import Response
from rapid_response_kit.utils.helpers import twilio_numbers


keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#']
start_menu = "Thank you for calling {}."
opt_say = "{}, press {}."
err_say = "Sorry, that's not a valid choice."
end_say = "Thank you for calling, goodbye."
voice = 'alice'


def install(app):
    app.config.apps.register('simplehelp', 'Simple Help Line', '/simplehelp')

    @app.route('/simplehelp', methods=['GET'])
    def show_simplehelp():
        numbers = twilio_numbers()
        return render_template("simplehelp.html", keys=keys, numbers=numbers)

    @app.route('/simplehelp', methods=['POST'])
    def do_simplehelp():

        data = parse_form(request.form)
        url = "{}/handle?{}".format(request.base_url, urlencode(data, True))

        r = Response()
        r.say('System is down for maintenance')
        fallback_url = echo_twimlet(r.toxml())

        try:
            client = twilio()
            client.phone_numbers.update(
                request.form['twilio_number'],
                friendly_name='[RRKit] Simple Help Line',
                voice_url=url,
                voice_method='GET',
                voice_fallback_url=fallback_url,
                voice_fallback_method='GET'
            )

            flash('Help menu configured', 'success')
        except Exception as e:
            print(e)
            flash('Error configuring help menu', 'danger')

        return redirect('/simplehelp')

    @app.route('/simplehelp/handle', methods=['GET'])
    def handle_menu():

        url = "{}?{}".format(request.base_url, request.query_string)

        response = Response()
        response.say(start_menu.format(request.args.get('name')), voice=voice)
        gather = response.gather(numDigits=1, action=url, method='POST')

        for key in keys:
            opt = request.args.get('opt_' + key)

            if opt is None:
                continue

            opt_args = opt.split(':')
            gather.say(opt_say.format(opt_args[1], key), voice=voice)

        return str(response)

    @app.route('/simplehelp/handle', methods=['POST'])
    def handle_opt():
        response = Response()

        digit = request.form['Digits']
        opt = request.args.get('opt_' + digit, None)

        if opt is None:
            response.say(err_say)
            response.redirect(
                "{}?{}".format(request.base_url, request.query_string))
            return str(response)

        opt_args = opt.split(':')

        if opt_args[0] == 'Call':
            response.dial(opt_args[2])
        elif opt_args[0] == 'Info':
            response.say(opt_args[2], voice=voice)
            response.say(end_say, voice=voice)

        return str(response)


def parse_form(form):
    data = {'name': form.get('menu_name', '')}

    for key in keys:
        if form.get('type_' + key, 'Inactive') == "Inactive":
            continue

        data['opt_' + key] = "{}:{}:{}".format(form['type_' + key],
                                               form['desc_' + key],
                                               form['value_' + key])

    return data
