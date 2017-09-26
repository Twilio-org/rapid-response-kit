/* global module, exports */
'use strict'

const twilio = require('twilio')

exports.handler = (context, event, callback) => {
  console.log(event)

  let twiml = new twilio.twiml.MessagingResponse()
  twiml.message('Hello, world!')
  callback(null, twiml)
}
