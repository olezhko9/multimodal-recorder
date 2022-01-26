from random import random

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

socketio = SocketIO(app, async_mode=None)


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")


@socketio.on('custom_event')
def handle_custom_event(json):
    print('received event: ' + str(json))


@socketio.on('connect')
def connected():
    print('Client connected')
    number = round(random() * 10, 3)
    emit('new_number', {'number': number})


if __name__ == "__main__":
    socketio.run(app, debug=True)
