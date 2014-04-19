from urllib import urlencode

from rapid_response_kit.utils.clients import twilio
from flask import render_template, request, redirect, flash
from rapid_response_kit.utils.helpers import parse_numbers, echo_twimlet, twilio_numbers
from rapid_response_kit.utils.voices import get_languages, is_valid_language, VOICES
from twilio.twiml import Response


def install(app):
    app.config.apps.register('ringdown', 'Ringdown', '/ringdown')

    @app.route('/ringdown', methods=['GET'])
    def show_ringdown():
        numbers = twilio_numbers()
        voices = VOICES.keys()
        languages = get_languages()
        return render_template("ringdown.html", numbers=numbers,
                               voices=voices, languages=languages)


    @app.route('/ringdown', methods=['POST'])
    def do_ringdown():
        numbers = parse_numbers(request.form.get('numbers', ''))
        data = {
            'stack': numbers,
            'sorry': request.form.get('sorry', '')
        }

        url = "{}/handle?{}".format(request.base_url, urlencode(data, True))

        twiml = '<Response><Say>System is down for maintenance</Say></Response>'
        fallback_url = echo_twimlet(twiml)

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
            voice_engine = request.form.get('voice-engine', 'man')
            voice_language = request.form.get('voice-language', 'en')

            if not is_valid_language(voice_engine, voice_language):
                flash('Please provide a valid language', 'danger')
                return redirect('/ringdown')

            resp = Response()
            resp.say(sorry, voice=voice_engine, language=voice_language)

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
