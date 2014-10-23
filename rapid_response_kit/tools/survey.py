import uuid

from rapid_response_kit.utils.clients import parse_connect, twilio
from clint.textui import colored
from flask import render_template, request, flash, redirect
from rapid_response_kit.utils.helpers import twilio_numbers, parse_numbers
from parse_rest.datatypes import Object as pObject
from twilio.twiml import Response


class SurveyResult(pObject):
    pass


def install(app):
    if not parse_connect(app.config):
        print(colored.red(
                    '''
                    Survey requires Parse.
                    Please add PARSE_APP_ID and PARSE_REST_KEY
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
        numbers = parse_numbers(request.form['numbers'])

        survey = uuid.uuid4()

        url = "{}/handle?survey={}".format(request.base_url, survey)

        client = twilio()

        try:
            client.phone_numbers.update(request.form['twilio_number'],
                                        sms_url=url,
                                        sms_method='GET',
                                        friendly_name='[RRKit] Survey')
        except:
            flash('Unable to update number', 'danger')
            return redirect('/survey')

        from_number = client.phone_numbers.get(request.form['twilio_number'])

        flash('Survey is now running as {}'.format(survey), 'info')

        body = "{} Reply YES / NO".format(request.form['question'])

        for number in numbers:
            try:
                client.messages.create(
                    body=body,
                    to=number,
                    from_=from_number.phone_number,
                    media_url=request.form.get('media', None)
                )
                flash('Sent {} the survey'.format(number), 'success')
            except Exception:
                flash("Failed to send to {}".format(number), 'danger')

        return redirect('/survey')

    @app.route('/survey/handle')
    def handle_survey():
        body = request.args['Body']
        normalized = body.strip().lower()

        result = SurveyResult.Query.filter(number=request.args['From'],
                                           survey_id=request.args['survey'])

        if result.count() > 0:
            resp = Response()
            resp.sms('Your response has been recorded')
            return str(resp)

        normalized = normalized if normalized in ['yes', 'no'] else 'N/A'

        result = SurveyResult(raw=body, normalized=normalized,
                              number=request.args['From'],
                              survey_id=request.args['survey'])

        result.save()

        resp = Response()
        resp.sms('Thanks for answering our survey')
        return str(resp)
