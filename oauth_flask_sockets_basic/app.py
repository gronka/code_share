from flask import Flask
from flask_socketio import SocketIO

from conf import conf


app = Flask(__name__)
app.secret_key = b'1111'
# TODO: enable cors before deployment?
socketio = SocketIO(app, cors_allowed_origins='*')
