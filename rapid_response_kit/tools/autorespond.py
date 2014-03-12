from rapid_response_kit.utils.clients import twilio
from flask import render_template, request, redirect, flash
from rapid_response_kit.utils.helpers import echo_twimlet, twilio_numbers


def install(app):
    app.config.apps.register('autorespond', 'Auto Respond', '/auto-respond')

    @app.route('/auto-respond', methods=['GET'])
    def show_auto_respond():
        numbers = twilio_numbers()
        return render_template("auto-respond.html", numbers=numbers)

    @app.route('/auto-respond', methods=['POST'])
    def do_auto_respond():
        sms_message = request.form.get('sms-message', '')
        voice_message = request.form.get('voice-message', '')

        if len(sms_message) == 0 and len(voice_message) == 0:
            flash('Please provide a message', 'danger')
            return redirect('/auto-respond')

        sms_url = ''
        voice_url = ''

        if len(sms_message) > 0:
            twiml = '<Response><Sms>{}</Sms></Response>'.format(sms_message)
            sms_url = echo_twimlet(twiml)

        if len(voice_message) > 0:
            twiml = '<Response><Say>{}</Say></Response>'.format(voice_message)
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