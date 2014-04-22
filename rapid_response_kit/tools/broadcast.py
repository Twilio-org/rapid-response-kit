from rapid_response_kit.utils.clients import twilio

from flask import render_template, request, flash, redirect
from rapid_response_kit.utils.helpers import parse_numbers, echo_twimlet, twilio_numbers
from rapid_response_kit.utils.voices import is_valid_language, VOICES


def install(app):
    app.config.apps.register('broadcast', 'Broadcast', '/broadcast')

    @app.route('/broadcast', methods=['GET'])
    def show_broadcast():
        numbers = twilio_numbers('phone_number')
        voices = VOICES.keys()
        return render_template("broadcast.html", numbers=numbers,
                               voices=voices)


    @app.route('/broadcast', methods=['POST'])
    def do_broadcast():
        numbers = parse_numbers(request.form.get('numbers', ''))
        message = request.form.get('message', '')
        voice_engine = request.form.get('voice-engine', 'man')
        voice_language = request.form.get('voice-language', 'en')
        twiml = '<Response><Say voice="{0}" language="{1}">{2}</Say></Response>'
        url = echo_twimlet(twiml.format(voice_engine, voice_language, message))

        if not is_valid_language(voice_engine, voice_language):
            flash('Please provide a valid language', 'danger')
            return redirect('/broadcast')

        client = twilio()

        for number in numbers:
            try:
                if request.form['method'] == 'sms':
                    client.messages.create(
                        body=request.form['message'],
                        to=number,
                        from_=request.form['twilio_number']
                    )
                else:
                    client.calls.create(
                        url=url,
                        to=number,
                        from_=request.form['twilio_number']
                    )
                flash("Sent {} the message".format(number), 'success')
            except Exception:
                flash("Failed to send to {}".format(number), 'danger')

        return redirect('/broadcast')
