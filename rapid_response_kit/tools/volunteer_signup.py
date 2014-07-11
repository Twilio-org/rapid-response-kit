import os.path
from flask import render_template, request, flash, redirect
from clint.textui import colored
import gdata.docs.data
import gdata.docs.client
import gdata.spreadsheet.service

from rapid_response_kit.utils.clients import twilio, get_google_creds
from rapid_response_kit.utils.helpers import parse_numbers, echo_twimlet, twilio_numbers
from twilio.twiml import Response

def install(app):
    (user, password) = get_google_creds(app.config)
    if user == None or password == None:
        print colored.red(
            'Volunteer Signup requires Google credentials, please add GOOGLE_ACCOUNT_USER and GOOGLE_ACCOUNT_PASS to your config.py')
        return

    app.config.apps.register('volunteer-signup', 'Volunteer Signup', '/volunteer-signup')

    spreadsheet_key = ''
    google_client = None

    @app.route('/volunteer-signup', methods=['GET'])
    def show_volunteer_signup():
        numbers = twilio_numbers()
        return render_template("volunteer-signup.html", numbers=numbers)


    @app.route('/volunteer-signup', methods=['POST'])
    def do_volunteer_signup():
        numbers = parse_numbers(request.form.get('numbers', ''))

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

        # create google spreadsheet
        global google_client
        (user, password) = get_google_creds(app.config)
        google_client = gdata.docs.client.DocsClient(source='VolunteerSignup')
        google_client.client_login(user, password, source='VolunteerSignup', service='writely')
        document = gdata.docs.data.Resource(type='spreadsheet', title=request.form.get('file-name', 'signup'))
        document = google_client.CreateResource(document)
        global spreadsheet_key
        spreadsheet_key = document.GetId().split("%3A")[1]

        # update column headers
        google_client = gdata.spreadsheet.service.SpreadsheetsService()
        google_client.ClientLogin(user, password)
        google_client.UpdateCell(1, 1, 'name', spreadsheet_key)
        google_client.UpdateCell(1, 2, 'phone', spreadsheet_key)
        google_client.UpdateCell(1, 3, 'response', spreadsheet_key)

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
        global drive
        global file_name
        response = Response()
        from_number = request.values.get('From')
        body = request.values.get('Body')

        row = {}
        (f_name, l_name, response) = body.strip().split(' ')
        row['name'] = f_name + ' ' + l_name
        row['phone'] = from_number
        row['response'] = response.upper()
        global google_client
        global spreadsheet_key
        google_client.InsertRow(row, spreadsheet_key)
     
        return str(response)


