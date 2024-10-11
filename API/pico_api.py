import base64

from flask import Flask, request
from flask_socketio import SocketIO, emit
from Crypto.Random import get_random_bytes
import threading
import random

from security.aes import AESecurity
from util.program_codes import AesMode

challenges = {}

clients = {}


def index():
    return "Welcome to Pico Signaling Server"


class API:
    def __init__(self):
        self._app = Flask(__name__)
        self._socketio = SocketIO(self._app)

        # AES instance
        self._aes = AESecurity(AesMode.PICO)

        # routes and event handlers
        self._app.add_url_rule('/', 'index', index)
        self._socketio.on_event('connect', self.handle_connect)
        self._socketio.on_event('response', self.handle_response)
        self._socketio.on_event('logs', self.pico_logs)

    def handle_connect(self):
        print("Client Connected")
        byte = get_random_bytes(16)
        challenge = base64.encodebytes(byte).decode("utf-8").strip()
        challenges[request.sid] = challenge
        self._socketio.emit('challenge', {'data': challenge})

    def handle_response(self, data):
        given_challenge = challenges[request.sid]
        encrypted_challenge = base64.b64decode(data['response'])
        nonce = base64.b64decode(data['nonce'])
        tag = base64.b64decode(data['tag'])
        if not given_challenge:
            self._socketio.emit('error', {'data': "Challenge not found."})
        decrypted_challenge = self._aes.decrypt(encrypted_challenge, tag, nonce)
        if decrypted_challenge == given_challenge:
            clients[request.sid] = True
            self._socketio.emit('success', {'data': "Successfully connected."})
        else:
            self._socketio.emit('error', {'data': "Authentication failed."})

    def pico_logs(self, event):
        print("Received message:", event)
        self._socketio.emit('response', {'data': "Message received."})

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

