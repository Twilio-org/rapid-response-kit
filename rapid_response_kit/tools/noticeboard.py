from rapid_response_kit.utils.clients import twilio

from flask import render_template, request, flash, redirect
from rapid_response_kit.utils.helpers import (
    parse_numbers,
    echo_twimlet,
    twilio_numbers)


def install(app):
    app.config.apps.register('noticeboard', 'Noticeboard', '/noticeboard')

    @app.route('/noticeboard', methods=['GET'])
    def show_noticeboard():
        numbers = twilio_numbers('phone_number')
        return render_template("noticeboard.html", url=request.base_url + '/live', numbers=numbers)


    @app.route('/noticeboard', methods=['POST'])
    def do_noticeboard():

        return redirect('/noticeboard')
