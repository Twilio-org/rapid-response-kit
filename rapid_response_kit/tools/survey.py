import uuid
import requests

from rapid_response_kit.utils.clients import twilio
from clint.textui import colored
from flask import render_template, request, flash, redirect
from rapid_response_kit.utils.helpers import twilio_numbers, parse_numbers
from twilio.twiml import Response


def install(app):
    if 'FIREBASE_URL' not in app.config or \
       'FIREBASE_SECRET' not in app.config:
        print(colored.red(
                    '''
                    Survey requires Firebase.
                    Please add FIREBASE_URL and FIREBASE_SECRET
                    to rapid_response_kit/utils/config.py
                    '''))
        return

    app.config.apps.register('survey', 'Survey', '/survey')

    @app.route('/survey', methods=['GET'])
    def show_survey():
        numbers = twilio_numbers()
        return render_template('survey.html', numbers=numbers)

    @app.route('/survey', methods=['POST'])
    def do_survey():
        survey = uuid.uuid4()
        twilio_client = twilio()
        twilio_number = request.form['twilio_number']
        numbers = parse_numbers(request.form['numbers'])
        sms_url = "{}/handle?survey={}".format(request.base_url, survey)

        try:
            twilio_client.phone_numbers.update(
                twilio_number,
                sms_url=sms_url,
                sms_method='GET',
                friendly_name='[RRKit] Survey'
            )
        except:
            flash('Unable to update number', 'danger')
            return redirect('/survey')

        flash('Survey is now running as {}'.format(survey), 'info')

        kwargs = {}
        kwargs['body'] = "{} Reply YES / NO".format(request.form['question'])
        kwargs['from_'] = twilio_client.phone_numbers.get(twilio_number).phone_number
        kwargs['media'] = request.form.get('media', None)
        if request.form.get('media', None):
            kwargs.pop('media')

        for number in numbers:
            kwargs['to'] = number
            try:
                twilio_client.messages.create(**kwargs)
                flash('Sent {} the survey'.format(number), 'success')
            except Exception:
                flash("Failed to send to {}".format(number), 'danger')

        return redirect('/survey')

    @app.route('/survey/handle')
    def handle_survey():
        body = request.args['Body']
        normalized = body.strip().lower()
        survey_id = request.args['survey']
        phone_number = request.args['From']

        json_url = '{firebase_url}/survey/{survey_id}/phone_number/{phone_number}.json'.format(
            firebase_url=app.config['FIREBASE_URL'],
            survey_id=survey_id,
            phone_number=phone_number)

        result = requests.get(json_url, params={'auth': app.config['FIREBASE_SECRET']}).json()
        if result:
            resp = Response()
            resp.sms('Your response has been recorded')
            return str(resp)

        normalized = normalized if normalized in ['yes', 'no'] else 'N/A'
        requests.post(json_url, params={'auth': app.config['FIREBASE_SECRET']}, json={
            'raw': body,
            'normalized': normalized,
            'number': request.args['From'],
            'survey_id': request.args['survey']
        })

        resp = Response()
        resp.sms('Thanks for answering our survey')
        return str(resp)
