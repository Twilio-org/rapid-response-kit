import os.path
from flask import render_template, request, flash, redirect
from clint.textui import colored
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from rapid_response_kit.utils.clients import twilio
from rapid_response_kit.utils.helpers import parse_numbers, echo_twimlet, twilio_numbers

def install(app):
    app.config.apps.register('volunteer-signup', 'Volunteer Signup', '/volunteer-signup')

    if not os.path.isfile('client_secrets.json'):
        print colored.red('Volunteer Signup requires Google Drive API, please add client_secrets.json to your working directory')

    file_name = 'signup.csv'
    drive = None

    @app.route('/volunteer-signup', methods=['GET'])
    def show_volunteer_signup():
        numbers = twilio_numbers()
        return render_template("volunteer-signup.html", numbers=numbers)


    @app.route('/volunteer-signup', methods=['POST'])
    def do_volunteer_signup():
        numbers = parse_numbers(request.form.get('numbers', ''))
        twiml = "<Response><Say>{}</Say></Response>"
        url = echo_twimlet(twiml.format(request.form.get('message', '')))

        # Update phone number url for replys
        url = "{}/handle?{}".format(request.base_url, request.query_string)
        twiml = '<Response><Say>System is down for maintenance</Say></Response>'
        fallback_url = echo_twimlet(twiml)

        try:
            client = twilio()
            client.phone_numbers.update(request.form['twilio_number'],
                                        friendly_name='[RRKit] Volunteer Signup',
                                        sms_url=url,
                                        sms_method='POST',
                                        sms_fallback_url=fallback_url,
                                        sms_fallback_method='GET')

            flash('Help menu configured', 'success')
        except Exception as e:
            print(e)
            flash('Error configuring phone number', 'danger')


        # Creates local webserver and auto handles authentication
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)

        file_name = request.form.get('file-name')

        # creates and uploads file
        file1 = drive.CreateFile({'title': file_name, 'mimeType':'text/csv'})
        file1.SetContentString('Name, Phone Number, Response')
        file1.Upload()

        client = twilio()
        # Since the value of the form is a PN sid need to fetch the number
        phoneNumber = client.phone_numbers.get(request.form['twilio_number'])

        for number in numbers:
            try:
                client.messages.create(
                    body=request.form['message'],
                    to=number,
                    from_= phoneNumber.phone_number
                )
                flash("Sent {} the message.".format(number), 'success')
            except Exception:
                flash("Failed to send to {}".format(number), 'danger')

        return redirect('/volunteer-signup')


    @app.route('/volunteer-signup/handle', methods=['POST'])
    def add_volunteer():
        response = Response()

        from_number = request.values.get('From')
        message = request.values.get('Mesage')

        # Parse message and add to gdoc
     
        return str(response)


