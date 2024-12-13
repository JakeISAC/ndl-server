import json

import paho.mqtt.client as mqtt
from threading import Thread
from api.user_api import UserApi
from api.members_api import MembersApi
from mqtt.message_handler import MessageHandler
from util.endpoints import Endpoints
from database.session_db import DbOperationsSession

class MQTTServer:
    def __init__(self):
        self._endpoints = Endpoints()
        self._user_api = UserApi()
        self._members_api = MembersApi()
        self._session_db = DbOperationsSession()
        self._on_message = MessageHandler(self.send_message).on_message
        # MQTT server config
        # broker here is the mosquito broker running on the pi
        self._broker = "localhost"
        self._topic = "weird-stuff"
        # set up MQTT client
        self._client = mqtt.Client()
        self._client.username_pw_set(self._endpoints.MQTT_USERNAME, self._endpoints.MQTT_PASSWORD)
        self._client.on_message = self._on_message
        self._connect()
        # subscribe to the topic I need to listen to
        self._client.subscribe("login_ask")
        self._client.subscribe("logs")
        self._client.subscribe("register")
        self._client.subscribe("add_member")

    def _connect(self):
        try:
            self._client.connect(self._broker)
        except Exception as e:
            raise e

    def _mqtt_loop(self):
        self._client.loop_start()

    def send_message(self, message, topic=None):
        if not topic:
            topic = self._topic
        self._client.publish(str(topic), str(message))

    def stop_mqtt(self):
        self._client.disconnect()

    def _run(self):
        self._mqtt_loop()

    def run(self):
        server_thread = Thread(target=self._run)
        server_thread.start()
