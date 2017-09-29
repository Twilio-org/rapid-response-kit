# SMS Broadcast

Use this app to broadcast SMS messages to large numbers of people.

## Install Link

[TODO - Console install link](#)

## Environment Configuration

| Variable | Description |
| --- | --- |
| `SB\_NOTIFY\_SERVICE\_SID` | The [Notify service](https://www.twilio.com/console/notify/services) you wish to use to send outbound SMS - must have a [Messaging Service](https://www.twilio.com/console/sms/services) associated with it (see docs below) |
| `SB_BROADCAST_ADMIN_NUMBERS` | A comma separated list of [E.164 formatted](https://en.wikipedia.org/wiki/E.164) phone numbers for people that can use the `broadcast` command. e.g. `+16512225555,+14156667777` |

## Required npm Modules

None - only built-in `twilio` module is used.

## Setup

Before using this Function, you will need to create (or use an existing) Notify service and Messaging service. The Notify service will use the Messaging service to send out SMS messages. The Messaging service will be configured to send incoming messages to your Subscribe/Broadcast function.

### Create a Messaging Service

Go to the console and [create a messaging service](https://www.twilio.com/console/sms/services). Choose the "Notifications, Two-way" use case to preset some options on the service.

Once created, click on the left nav link for "Numbers" and add (or buy) a phone number to use with this service. This will be the phone number(s) your end users will interact with.

We'll need to come back here later - consider leaving this page open in a tab while you proceed to the next step in the console.

### Create a Notify Service

In the console, create a [Notify service](https://www.twilio.com/console/notify/services). Our function code uses Notify to store our subscriber list and to send out notifications. After your service is created, locate the Dropdown in your Notify service config labeled "Messaging Service SID". You should be able to choose the Messaging Service we created in the last step. 

You will need the generated SID for this service to configure your environment in the next step.

Don't forget to save your changes!

### Configure your environment variables

In the console, [go to the Functions configuration page](https://www.twilio.com/console/runtime/functions/configure). Create the two environment variables listed in the table at the top of the page. Use the Notify service SID from the last step for the first variable. For the second, enter a list of phone numbers for "administrators" of the application who will be able to use the `broadcast` command to send messages out to the entire group. The variable changes should auto-save.

Now we're ready to deploy our Function.

### Create the Broadcast/Subscribe Function

In the console, [go to the Functions page](https://www.twilio.com/console/runtime/functions/manage) and create a new Blank function. 

Paste in the code from the [`sb_broadcast`](../functions/sb_broadcast.js) example function in the Rapid Response Kit repository in the browser text editor. Give the Function the route `/sb_broadcast`. Copy the final Function URL to your clipboard, as you will need it in the final configuration step.

Hit the "Save" button to deploy your Function!

### Handle incoming messages with your Function

Go back to the [messaging service](https://www.twilio.com/console/sms/services) you created earlier. In its configuration, you'll see a checkbox for "Handle Incoming Messages". Click this box to enable the feature. In the text box that appears, paste in the URL to the Function we just deployed. Click "Save".

Now if all went well, you'll be able to start using your phone number for managing broadcasts and subscriptions!

## Usage

Once your phone number is set up, folks can text anything to it to receive a brief informational message about what commands are available.

* `subscribe` - subscribes the current number for updates from the service
* `stop` - uses Twilio's built-in stop handling to prevent a user from receiving messages
* `start` - uses Twilio's built-in features to opt a user back in to receiving messages
* `broadcast <message content>` - Administrators can use the broadcast command to send a message out to all subscribed users. Not included in help text.

To edit the copy for any of the messages, open the `sb_broadcast` function code and look for the text strings at the top of the file.
