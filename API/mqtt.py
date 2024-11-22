from lib2to3.pgen2.tokenize import endprogs

import paho.mqtt.client as mqtt
import time
import threading

from API.user_api import UserApi
from util.endpoints import Endpoints
from util.program_codes import UserLoginResponse as user_codes


class MQTTServer:
    def __init__(self):
        self._endpoints = Endpoints()
        self._user_api = UserApi()
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
        self._client.subscribe("login")
        self._client.subscribe("magnetic_lock")
        # endpoints to user API
        self._login = "login"
        self._register = "register"
        self._add_member = "add_member"
        self._lock_status = "lock_status"
        self._last_active_person = "last_active_person"
        self._change_password = "change_password"
        self._all_members = "all_members"
        self._change_member = "change_member_data"

    def _on_message(self, client, userdata, msg):
        match msg.topic:
            case "login":
                payload = msg.payload.decode()
                print(payload)
                if self._user_api.login(str(payload)):
                    print("Hi")
                    self.send_message(user_codes.OK, "login_response")
                else:
                    print(":(")
                    self.send_message(user_codes.FAILED, "login_response")
                print(payload)
            case "magnetic_lock":
                payload = msg.payload.decode()
                print(payload)
            case _:
                pass

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

    # subscriber; topic: logs
    def logs_dump(self):
        pass

    # subscriber; topic: lock_status
    def lock_status(self):
        pass

    def _run(self):
        self._mqtt_loop()
        while True:
            pass

    def stop_mqtt(self):
        self._client.loop_stop()
        self._client.disconnect()

    def run(self):
        server_thread = threading.Thread(target=self._run)
        server_thread.start()
