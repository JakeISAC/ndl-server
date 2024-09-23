from flask import Flask, request
from flask_socketio import SocketIO, emit
import threading


def index():
    return "Pico Signaling Server"


class API:
    def __init__(self):
        self._app = Flask(__name__)
        self._socketio = SocketIO(self._app)

        # routes and event handlers
        self._app.add_url_rule('/', 'index', index)
        self._socketio.on_event('connect', self.handle_connect)
        self._socketio.on_event('message', self.handle_message)

    def handle_connect(self):
        print("Client Connected")
        self._socketio.emit('response', {'data': "Connected to the server"})

    def handle_message(self, msg):
        print("Received message:", msg)
        self._socketio.emit('response', {'data': "Message received"})

    def send_message(self, event, message):
        self._socketio.emit(event, {'data': message})

    def run(self):
        socketio_thread = threading.Thread(target=lambda: self._socketio.run(
            self._app, host="localhost", port=8080, allow_unsafe_werkzeug=True
        ))
        socketio_thread.start()

