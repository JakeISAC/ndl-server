import json

import paho.mqtt.client as mqtt
from threading import Thread
from api.user_api import UserApi
from api.members_api import MembersApi
from domains.member import Member
from util.endpoints import Endpoints
from util.program_codes import UserLoginResponse as UserCodes
from util.program_codes import AddMemberResponse as MemberResponse
from database.session_db import DbOperationsSession

class MQTTServer:
    def __init__(self):
        self._endpoints = Endpoints()
        self._user_api = UserApi()
        self._members_api = MembersApi()
        self._session_db = DbOperationsSession()
        # MQTT server config
        # broker here is the mosquito broker running on the pi
        self._broker = "localhost"
        self._topic = "weird-stuff"
        # set up MQTT client
        self._client = mqtt.Client()
        self._client.username_pw_set(self._endpoints.MQTT_USERNAME, self._endpoints.MQTT_PASSWORD)
        self._client.on_message = self._on_message
        self._connect()
        # endpoints to user api
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
        self._client.subscribe(self._register)
        self._client.subscribe(self._add_member)

    def _on_message(self, client, userdata, msg):
        match msg.topic:
            case self._logs:
                payload = msg.payload.decode()
                print(payload)
            case self._login:
                payload = msg.payload.decode()
                print(payload)
                success, token = self._user_api.login(str(payload))
                response = {'code': str(UserCodes.OK), 'session_token': None}
                if success:
                    response['session_token'] = token
                    self.send_message(json.dumps(response), "login_response")
                else:
                    self.send_message(json.dumps(response), "login_response")
            case self._register:
                payload = msg.payload.decode()
                print(payload)
                if self._user_api.register(str(payload)):
                    self.send_message(str(UserCodes.OK), "register_response")
                else:
                    self.send_message(str(UserCodes.FAILED), "register_response")
            case self._magnetic_lock:
                payload = msg.payload.decode()
                print(payload)
            case self._add_member:
                payload = msg.payload.decode()
                payload_parsed = json.loads(payload)
                member = payload_parsed['value']
                session_token = payload_parsed['session_token']
                if self._session_db.check_token(session_token):
                    member_extracted = Member.extract_member(member)
                    self._members_api.add_member(member_extracted)
                    self.send_message(str(MemberResponse.OK), "add_member_response")
                else:
                    self.send_message(str(MemberResponse.FAILED), "add_member_response")
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
