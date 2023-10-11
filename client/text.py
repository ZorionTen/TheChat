import eel

# Set the web folder and define the initial HTML file
eel.init('web_dev')

# Expose a Python function to be called from JavaScript


@eel.expose
def greet_from_python(name):
    return f'Hello, {name}!'

eel.start('index.html', size=(800, 600))

