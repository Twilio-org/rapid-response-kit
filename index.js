/* Test server for local development */
'use strict'

// Load environment configuration
require('dotenv').config()

// Test harness dependencies
const http = require('http')
const twilio = require('twilio')
const express = require('express')
const urlencoded = require('body-parser').urlencoded

// Create Express app to serve assets and execute functions
const app = express()
app.use(express.static(`${__dirname}/assets`))
app.use(urlencoded({ extended: false }))

// By default functions listen on all HTTP methods (at least GET and POST)
app.all('/:function', (request, response) => {
  // Attempt to load function for URL
  let fn = null
  try {
    fn = require(`./functions/${request.params.function}`)
  } catch (e) {
    console.log(e)
    response.status(404)
    return response.send('Could not load function - see console for details.')
  }

  // Combine query parameters and POST body into single event object
  let event = Object.assign({}, request.query, request.body)

  // Execute function provided
  fn.handler(process.env, event, (err, result) => {
    // Callback passed to function
    if (err) {
      response.status(500)
      return response.send(err)
    }

    // If it's a TwiML object, render appropriately - if not, let Express
    // sort it out
    if (result.constructor === twilio.twiml.VoiceResponse ||
        result.constructor === twilio.twiml.MessagingResponse) {
      response.type('text/xml')
      response.send(result.toString())
    } else {
      response.send(result)
    }
  })
})

// Run on configurable port
const port = process.env.PORT || 3000
const server = http.createServer(app)
server.listen(port, () => {
  console.log('Twilio Function test harness running on *:', port)
})
