# Twilio.org Rapid Response Kit Contributor's Guide

This guide provides you with the information necessary to make a Tool for the
Twilio.org Rapid Response Kit.

## Anatomy of a Tool

A Tool in the Twilio.org Rapid Response Kit contains a few simple components.

### Python Module

A Tool is just a module that has a single top-level function, `install`  This
function will be called when the application starts, it will be passed the flask
application instance.

#### Registering

The `install` function should perform any prerequisite checks, if any fail it is
permitted to output an error message and then should simply return (this allows
for a Tool to fail to register but not take out the entire Rapid Response Kit).

If the prerequisite checks pass, then the Tool should make a call to the app's
config object to register itself.

Example:
app.config.apps.register('example', 'Example Tool', '/example')

The first argument is a key, it uniquely identifies the Tool.  The second
argument is the Display Name for the Tool, it will be used in console output and
in the Web UI.  The third argument is the relative path to serve the tool at.

By calling register the Rapid Response Kit will then add your app to the global
navigation and output the successful installation message in the console output.

#### Adding endpoints

The `install` function should then define new flask endpoints, always under the
relative path.  For our example Tool, the following convention is used.

```python
@app.route('/example', methods=['GET'])
def show_example():
    # code to display the example page

@app.route('/example', methods=['POST'])
def do_example():
    # code to perform the example Tools purpose

# Optional
@app.route('/example/handle', methods=[...])
def handle_example():
    # code to handle incoming traffic
```