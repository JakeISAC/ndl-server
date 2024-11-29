import paho.mqtt.client as mqtt
from threading import Thread
from API.user_api import UserApi
from util.endpoints import Endpoints
from util.program_codes import UserLoginResponse as UserCodes


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
        # endpoints to user API
        self._login = "login_ask"
        self._register = "register"
        self._add_member = "add_member"
        self._lock_status = "lock_status"
        self._last_active_person = "last_active_person"
        self._change_password = "change_password"
        self._all_members = "all_members"
        self._change_member = "change_member_data"
        self._delete_member = "delete_member"
        # endpoint controller
        self._magnetic_lock = "magnetic_lock" # publisher
        self._logs = "logs" # subscriber
        # subscribe to the topic I need to listen to
        self._client.subscribe(self._login)
        self._client.subscribe(self._logs)

    def _on_message(self, client, userdata, msg):
        match msg.topic:
            case "logs":
                payload = msg.payload.decode()
                print(payload)
            case "login_ask":
                payload = msg.payload.decode()
                print(payload)
                if self._user_api.login(str(payload)):
                    self.send_message(UserCodes.OK, "login_response")
                else:
                    self.send_message(UserCodes.FAILED, "login_response")
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

    def stop_mqtt(self):
        self._client.disconnect()

    def _run(self):
        self._mqtt_loop()

    def run(self):
        server_thread = Thread(target=self._run)
        server_thread.start()
