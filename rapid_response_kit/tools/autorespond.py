from rapid_response_kit.utils.clients import twilio
from flask import render_template, request, redirect, flash
from rapid_response_kit.utils.helpers import echo_twimlet, twilio_numbers
from rapid_response_kit.utils.voices import get_languages, is_valid_language, VOICES


def install(app):
    app.config.apps.register('autorespond', 'Auto Respond', '/auto-respond')

    @app.route('/auto-respond', methods=['GET'])
    def show_auto_respond():
        numbers = twilio_numbers()
        voices = VOICES.keys()
        languages = get_languages()
        return render_template("auto-respond.html", numbers=numbers,
                               voices=voices, languages=languages)

    @app.route('/auto-respond', methods=['POST'])
    def do_auto_respond():
        sms_message = request.form.get('sms-message', '')
        voice_message = request.form.get('voice-message', '')
        voice_engine = request.form.get('voice-engine', 'man')
        voice_language = request.form.get('voice-language', 'en')

        if len(sms_message) == 0 and len(voice_message) == 0:
            flash('Please provide a message', 'danger')
            return redirect('/auto-respond')

        if not is_valid_language(voice_engine, voice_language):
            flash('Please provide a valid language', 'danger')
            return redirect('/auto-respond')

        sms_url = ''
        voice_url = ''

        if len(sms_message) > 0:
            twiml = '<Response><Sms>{}</Sms></Response>'.format(sms_message)
            sms_url = echo_twimlet(twiml)

        if len(voice_message) > 0:
            twiml = """<Response>
                        <Say voice="{0}" language="{1}">{2}</Say>
                    </Response>""".format(voice_engine,
                                          voice_language,
                                          voice_message)
            voice_url = echo_twimlet(twiml)

        try:
            client = twilio()
            client.phone_numbers.update(request.form['twilio_number'],
                                        friendly_name='[RRKit] Auto-Respond',
                                        voice_url=voice_url,
                                        voice_method='GET',
                                        sms_url=sms_url,
                                        sms_method='GET')

            flash('Auto-Respond has been configured', 'success')
        except Exception:
            flash('Error configuring number', 'danger')

        return redirect('/auto-respond')
