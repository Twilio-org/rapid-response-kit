from rapid_response_kit.utils.clients import twilio

from flask import render_template, request, flash, redirect
from rapid_response_kit.utils.helpers import parse_numbers, echo_twimlet, twilio_numbers


def install(app):
    app.config.apps.register('log', 'Phone Log', '/log')

    @app.route('/log', methods=['GET'])
    def show_log():
        client = twilio()

        smsnumlist = []
        for sms in client.sms.messages.list():
            smsnumlist.append(sms.to)
            smsnumlist.append(sms.from_)


        callnumlist = []
        for call in client.calls.list():
            callnumlist.append(sms.to)
            callnumlist.append(sms.from_)

        smsnumlist = list(set(smsnumlist))
        callnumlist = list(set(callnumlist))

        numbers = twilio_numbers('phone_number')

        for num in numbers:
                if num in callnumlist:
                    callnumlist.remove(num)
                if num in smsnumlist:
                    smsnumlist.remove(num)


        return render_template("log.html", smsnumlist=smsnumlist, callnumlist=callnumlist)


    @app.route('/log', methods=['POST'])
    def do_log():
        numbers = parse_numbers(request.form.get('numbers', ''))
        twiml = "<Response><Say>{}</Say></Response>"
        url = echo_twimlet(twiml.format(request.form.get('message', '')))

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

        return redirect('/log')