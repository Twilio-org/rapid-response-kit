#The Twilio.org Rapid Response Kit

The Twilio.org Rapid Response Kit is a collection of open source communications tools any developer or technically inclined user can deploy quickly. Scroll down to INSTALLATION to get started.

Twilio.org is an initiative of the communications API platform company Twilio. Our mission is to provide nonprofit organizations with communications technologies to help them reach their goals and further the impact of social good.

If you are a qualified nonprofit, apply at Twilio.org/apply. Find other open source tools and resources at twilio.org/resources

## Prerequisites

Twilio Rapid Response Kit is a built on `python` and the `flask microframework`.
It uses `virtualenv` to sandbox the Twilio Rapid Response Kit from the rest of
your development or server environment. Twilio Rapid Response Kit uses `pip` to
resolve and install dependencies.

Please make sure that before you begin you meet the minimum requirements:

- Python 2.7
- virtualenv
- pip

## Tools available out-of-the-box

Twilio.org Rapid Response Kit comes with several tools already installed. When you
start up the Twilio.org Rapid Response Kit it will report what tools are available
and where. Below is a brief description of every tool provided.

### Auto-Respond
Use this tool to set up an recorded auto-responder to inbound voice calls or text messages. Respond to voice calls with a spoken message or to an incoming SMS message with a response SMS.

Useful for setting up and updating information lines.

### Broadcast
A simple messaging broadcast app. Send a one-way communications blast to a defined group of contacts.

Useful for broadcasting information to volunteers.

### Conference Line
Configures a Twilio Number to behave like a conference line. Anyone who calls
into the conference line will be dropped into a conference room. Supports
whitelisting numbers and multiple conference rooms.

### Forwarder
Forwards all voice traffic from a Twilio Number to a given Phone Number.

Useful for temporary public phone numbers.

### Ringdown
A tool that allows you to dial one number, which then will sequentially dial down a list of prioritized contacts until one of those contacts answer. You are able to set up contact lists ahead of time and if no one answers an optional message will be spoken.

Useful for setting up ad-hoc response teams and rudimentary call centers.

### Simple Help Line
Use this interactive voice response app to set up simple options for callers to press a number for information, or to connect to a pre-determined agent. Each key on the dialpad can be configured to either dial a Phone Number or provide
information.

Useful for setting up simple phone menus a la "Press 1 to call the Site Manager,
Press 2 to hear shelter hours, etc"

### Survey
**Survey requires integration with Parse to record results**.

An SMS-powered survey app to send out questions to a specified list of numbers and gather responses. You define the response parameters. Survey is similar to Broadcast but instead of broadcasting an informational
message, it broadcasts a yes / no question. Responses will be recorded in Parse
for analysis and action.

Useful for quick status and safety checks. Ex: "Can you help at 12th Street
Response Center?"

#### Getting Parse Keys

* [Create a free Parse application here](https://parse.com/)

* Navigate to [https://www.parse.com/apps/](https://www.parse.com/apps/) and create a new application.

* Click on the settings icon for the application:

![Parse app settings icon](http://i.imgur.com/zTPgBX9.png)

* Find the keys in the Key panel:

![Parse app key panel](http://i.imgur.com/GS9ISbU.png)

* Add your parse keys to the file rapid_response_kit/utils/config.py like so:

```
PARSE_APP_ID =  'Application ID'
PARSE_REST_KEY = 'REST API key'
```

### Town Hall
With this group conference call tool, an organizer can dial one number which then dials a list of predefined contacts. Individuals who answer the call are dropped into the same conference. This can handle up to 40 people in one conference call.

Useful for quickly gathering key stakeholders together for conference calls
without requiring everyone to dial into a predefined number.

### Volunteer Signup
**Volunteer Signup requires Google credentials to record results.**
Broadcast an sms message to a group of numbers with a volunteer opportunity and record responses to a Google spreadsheet.

Useful for quickly signing up volunteers and easily determining who is available to show up.

Note : If your Google account has 2-factor authentication enabled, you may need to [generate an application specific password](https://support.google.com/accounts/answer/185833?hl=en).

#### Gettin Google account credentials

* If you're **not** using 2-factor auth, just use your username and password. Be careful not to share them!

* If you are using 2-factor authenthication, [visit the app passwords page here](https://security.google.com/settings/security/apppasswords)

* After signing in, choose "custom app" from the "select app" dropdown menu:

![Drop down menu](http://i.imgur.com/NedCQaY.png)

* Name your application and click generate to get your new Google password:

![Google password](http://i.imgur.com/aRZRKBR.png)

* Copy your email and new password into rapid_response_kit/utils/config.py like so:

```
GOOGLE_ACCOUNT_USER = 'email'
GOOGLE_ACCOUNT_PASS = 'password'
```

### Noticeboard

**Noticeboard requires Pusher credentials for realtime updates**
Noticeboard is a virtual noticeboard where people can send MMS pictures of missing people, damaged items, or useful information to a publicly accessible webpage that will update in realtime as it receives MMS messages, allowing people in disaster relief to share information.

This tool was developed using the brand new MMS messaging capabilities at Twilio.

Noticeboard is a perfect tool to have running in disaster relief centers where people might congregate.

#### Getting Pusher keys

* [Sign up for a free account as pusher.com](pusher.com)

* Go to the [app page](https://app.pusher.com/) and click on "new app":

![pusher new app](http://i.imgur.com/dSpp9MJ.png)

* Name it, do not click on any other options, and click "create app".

* Your Pusher keys will be displayed on the right hand side of the page. Copy and paste them into rapid_response_kit/utils/config.py like so:

```
PUSHER_APP_ID='app_id'
PUSHER_KEY='key'
PUSHER_SECRET='secret'
```

## Installation

To install Twilio Rapid Response Kit to your development environment for testing
or development work, you can follow these simple steps.

1.  Download or git clone this project.
2.  From the project directory run `make install` on the command line
3.  During installation you will be prompted for your Twilio Account
  credentials, you can access these credentials from your [Twilio Account
 	Dashboard] (https://www.twilio.com/user/account).  If you don't have a
 	Twilio Account yet you can [sign up for a free trial account](https://www.twilio.com/try-twilio)

Once the Twilio Rapid Response Kit is installed, you can run it in debug
mode by running the `make debug` command from the Twilio Rapid Response Kit
folder.  This will start the application running on
[http://localhost:5000](http://localhost:5000).

## Stateless Design

You may have noticed that we haven't discussed what database Twilio.org Rapid
Response Kit uses yet. This is because Twilio.org Rapid Response Kit is comprised
of stateless tools that do not require a database to maintain the application
state.

This was a conscious design decision, Twilio.org Rapid Response Kit does not require
a database to function and therefore does not require the overhead generally
associated with administering a database.

## Just the beginning

These sample tools are just the beginning, if you want to extend Twilio.org Rapid
Response Kit to do more, please read our [Contributor's Guide] contributors.md)

This kit, and all other repos in the Twilio.org Github are open source. If you’d like to be a contributor to this project please contact ebalbuena@twilio.com

## Deploying

Once you have evaluated Twilio.org Rapid Response Kit and are happy with its
functionality, it's time to deploy it. For Twilio.org Rapid Response Kit to
function correctly it must be able to communicate with Twilio and vice-versa, so
it must be on a publicly accessible server.

### Your own hardware

To deploy Twilio.org Rapid Response Kit on your own server you can follow the same
installation guide. The flask server is not meant for production deployment, we
suggest running the Twilio.org Rapid Response Kit via uwsgi and forwarding to it
from nginx.

### Heroku

#### Running locally

1. `pip install gunicorn`
2. Create local_config.py with your environment variables and add to .gitignore
3. run `foreman start`

#### Deploying on Heroku

Click the button below to automatically set up the Rapid Response Kit in an app running on your Heroku account. You will be prompted to enter your Twilio credentials during setup.

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

Alternatively, you can manually create a Heroku app and use Git to push and deploy.

## Meta
No warranty expressed or implied. Software is as is.
MIT License
Powered by Twilio.org


The Twilio.org Rapid Response Kit is just a flask app, so feel free to deploy as you
would any flask application.
