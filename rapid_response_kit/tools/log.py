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
            callnumlist.append(call.to)
            callnumlist.append(call.from_)

        smsnumlist = list(set(smsnumlist))
        callnumlist = list(set(callnumlist))

        numbers = twilio_numbers('phone_number')

        for num in numbers:
                if num in callnumlist:
                    callnumlist.remove(num)
                if num in smsnumlist:
                    smsnumlist.remove(num)
        typeNum = "All Numbers"
        return render_template("log.html", smsnumlist=smsnumlist, callnumlist=callnumlist, numbers=numbers, typeNum=typeNum)


    @app.route('/log', methods=['POST'])
    def do_log():
        filternum = request.form['twilio_number']
        numbers = twilio_numbers('phone_number')
        typeNum = str(filternum)
        client = twilio()

        smsnumlist = []
        for sms in client.sms.messages.list():
            if sms.to == filternum:
                smsnumlist.append(sms.from_)
            elif sms.from_ == filternum:
                smsnumlist.append(sms.to)

        callnumlist = []
        for call in client.sms.messages.list():
            if call.to == filternum:
                callnumlist.append(call.from_)
            elif call.from_ == filternum:
                callnumlist.append(call.to)

        smsnumlist = list(set(smsnumlist))
        callnumlist = list(set(callnumlist))

        return render_template("log.html", smsnumlist=smsnumlist, callnumlist=callnumlist, numbers=numbers, typeNum=typeNum)