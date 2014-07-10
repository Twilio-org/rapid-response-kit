from rapid_response_kit.utils.clients import twilio

from flask import render_template, request, flash, redirect
from rapid_response_kit.utils.helpers import parse_numbers, echo_twimlet, twilio_numbers

def install(app):
    app.config.apps.register('volunteer-signup', 'Volunteer Signup', '/volunteer-signup')

    @app.route('/volunteer-signup', methods=['GET'])
    def show_volunteer_signup():
        numbers = twilio_numbers('phone_number')
        return render_template("volunteer-signup.html", numbers=numbers)


    @app.route('/volunteer-signup', methods=['POST'])
    def do_volunteer_signup():
        numbers = parse_numbers(request.form.get('numbers', ''))
        twiml = "<Response><Say>{}</Say></Response>"
        url = echo_twimlet(twiml.format(request.form.get('message', '')))

        client = twilio()

        for number in numbers:
            try:
                client.messages.create(
                    body=request.form['message'],
                    to=number,
                    from_=request.form['twilio_number']
                )
                flash("Sent {} the message. Here is the link to the spreadsheet ...".format(number), 'success')
            except Exception:
                flash("Failed to send to {}".format(number), 'danger')

        return redirect('/volunteer-signup')
