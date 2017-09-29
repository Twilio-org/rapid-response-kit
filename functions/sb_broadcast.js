/* global module, exports, require, process, console */
'use strict'

// Configure necessary Twilio objects
const twilio = require('twilio')
const client = twilio(process.env.ACCOUNT_SID, process.env.AUTH_TOKEN)
const notify = client.notify.services(process.env.SB_NOTIFY_SERVICE_SID)

// List of admin phone numbers should be in the system environment
const adminNumbers = process.env.SB_BROADCAST_ADMIN_NUMBERS

// Response strings - update these to change the copy in the messages
const helpMessage = 'Hello! Text "subscribe" to receive updates, "stop" to stop getting messages, and "start" to receive them again.'
const subscribeSuccessMessage = 'Thanks! You have been subscribed for updates.'
const subscribeFailMessage = 'Dang it. We couldn\'t subscribe you - try again later?'
const broadcastNotAuthorizedMessage = 'Your phone number is not authorized to broadcast in this application'
const broadcastSuccessMessage = 'Boom! Message broadcast to all subscribers.'
const broadcastFailMessage = 'Well this is awkward. Your message failed to send, try again later.'

// Helper class for commands
class Command {
  // Create a new instance with necessary arguments from the incoming SMS
  constructor(event, context) {
    this.fromNumber = event.From
    this.body = event.Body || ''
    this.event = event
    this.context = context

    // Occassionally, US numbers will be passed without the preceding
    // country code - check for this eventuality and fix it
    if (this.fromNumber.indexOf('+') !== 0) {
      this.fromNumber = `+1${this.fromNumber}`
    }
  }

  // Get an array of arguments after the first word for a command
  get commandArguments() {
    return this.body.trim().split(' ').slice(1)
  }

  // Get the full text after the command with spaces reinserted
  get commandText() {
    return this.commandArguments.join(' ')
  }

  // Execute command async (to be overridden by subclasses)
  run(callback) {
    callback(null, 'Command not implemented.')
  }
}

/* Subclasses for supported commands */

class HelpCommand extends Command {
  run(callback) {
    callback(null, helpMessage)
  }
}

class SubscribeCommand extends Command {
  run(callback) {
    // Create a new SMS Notify binding for this user's phone number
    notify.bindings.create({
      identity: this.fromNumber,
      bindingType: 'sms',
      address: this.fromNumber
    }).then((response) => {
      callback(null, subscribeSuccessMessage)
    }).catch(err => {
      callback(err, subscribeFailMessage)
    })
  }
}

class BroadcastCommand extends Command {
  run(callback) {
    // Check if sender is in list of admins, stored in the system environment
    // as a comma-separated string
    if (adminNumbers.indexOf(this.fromNumber) < 0) {
      return callback(null, broadcastNotAuthorizedMessage)
    }

    // Create a new SMS Notify binding for this user's phone number
    notify.notifications.create({
      tag: 'all',
      body: this.commandText
    }).then((response) => {
      callback(null, broadcastSuccessMessage)
    }).catch(err => {
      console.log(err)
      callback(err, broadcastFailMessage)
    })
  }
}

// Handle incoming SMS commands
exports.handler = (context, event, callback) => {
  // Get command text from incoming SMS body
  let cmd = event.Body || ''
  cmd = cmd.trim().split(' ')[0].toLowerCase()

  // Default to help command
  let cmdInstance = new HelpCommand(event, context)

  // Choose other commands as appropriate
  switch(cmd) {
    case 'subscribe': cmdInstance = new SubscribeCommand(event, context); break;
    case 'broadcast': cmdInstance = new BroadcastCommand(event, context); break;
  }

  // Execute command
  cmdInstance.run((err, message) => {
    let twiml = new twilio.twiml.MessagingResponse()
    if (err) {
      console.log(err)
      message = 'There was a problem with your request. Try again!'
    }
    twiml.message(message)
    callback(null, twiml)
  })
}
