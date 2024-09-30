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
        self._socketio.on_event('logs', self.pico_logs)

        # secure connection
        self._secure = False

    def handle_connect(self):
        print("Client Connected")
        self._socketio.emit('response', {'data': "Connected to the server"})

    def pico_logs(self, event):
        print("Received message:", event)
        self._socketio.emit('response', {'data': "Message received"})

    def send_message(self, event, message):
        if self._secure:
            self._socketio.emit(event, {'data': message})
        else:
            self._socketio.emit('error', {'data': 'You are not authorized.'})

    def run(self):
        socketio_thread = threading.Thread(target=lambda: self._socketio.run(
            self._app, host="localhost", port=8080, allow_unsafe_werkzeug=True
        ))
        socketio_thread.start()

