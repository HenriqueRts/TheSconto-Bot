from flask import Flask

app = Flask('')

@app.route('/')
def home():
    return "TheSconto bot is running!"

@app.route('/ping')
def ping():
    return "pong"

def keep_alive():
    app.run(host='0.0.0.0', port=8080)
