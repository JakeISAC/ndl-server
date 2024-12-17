import json
from api.user_api import UserApi
from api.members_api import MembersApi
from database.session_db import DbOperationsSession
from domains.member import Member
from util.endpoints import Endpoints
from util.program_codes import UserLoginResponse as UserCodes
from util.program_codes import AddMemberResponse as MemberResponse
from util.program_codes import DeleteResponse as DeleteCodes

# TODO: Add proper logs for exception handling

class MessageHandler:
    def __init__(self, send_message):
        self._endpoints = Endpoints()
        self._user_api = UserApi()
        self._members_api = MembersApi()
        self._session_db = DbOperationsSession()
        self._send_message = send_message # function
        # endpoints to user api
        self._login = "login_ask"
        self._register = "register"
        self._add_member = "add_member"
        self._lock_status = "lock_status"
        self._last_active_person = "last_active_person" # DONE in the Security module
        self._change_password = "change_password"
        self._all_members = "all_members"
        self._change_member = "change_member_data"
        self._delete_member = "delete_member"
        # endpoint controller
        self._magnetic_lock = "magnetic_lock"  # publisher
        self._logs = "logs"  # subscriber
        self._lock = "lock"
        self._rfid_response = "rfid_response"

    def on_message(self, _, userdata, msg):
        payload = msg.payload.decode()
        match msg.topic:
            case self._login:
                self._handle_login(payload)
            case self._register:
                self._handle_register(payload)
            case self._magnetic_lock:
                print(payload)
            case self._add_member:
                self._handle_add_member(payload)
            case self._all_members:
                self._handle_all_members(payload)
            case self._delete_member:
                self._handle_delete_member(payload)
            case _:
                pass

    def _handle_login(self, payload):
        try:
            print(payload)
            token = self._user_api.login(str(payload))
            response = {'code': str(UserCodes.FAILED), 'session_token': None}
            if token:
                response['code'] = str(UserCodes.OK)
                response['session_token'] = token
                self._send_message(json.dumps(response), "login_response")
            else:
                self._send_message(json.dumps(response), "login_response")
        except Exception:
            response = {'code': str(UserCodes.FAILED), 'session_token': None}
            self._send_message(json.dumps(response), "login_response")

    def _handle_register(self, payload):
        try:
            print(payload)
            payload_parsed = json.loads(payload)
            user = payload_parsed['value']
            session_token = payload_parsed['session_token']
            # check authentication
            if not self._session_db.check_token(session_token):
                raise Exception("Session token is invalid.")

            if self._user_api.register(str(user)):
                self._send_message(str(UserCodes.OK), "register_response")
            else:
                self._send_message(str(UserCodes.FAILED), "register_response")
        except Exception:
            self._send_message(str(UserCodes.FAILED), "register_response")

    def _handle_add_member(self, payload):
        try:
            payload_parsed = json.loads(payload)
            member = payload_parsed['value']
            session_token = payload_parsed['session_token']
            # check authentication
            if self._session_db.check_token(session_token):
                raise Exception("Session token is invalid.")

            member_extracted = Member.extract_member(member)
            self._members_api.add_member(member_extracted)
            self._send_message(str(MemberResponse.OK), "add_member_response")
        except Exception:
            self._send_message(str(MemberResponse.FAILED), "add_member_response")

    def _handle_all_members(self, payload):
        try:
            print(payload)
            payload_parsed = json.loads(payload)
            session_token = payload_parsed['session_token']
            # check authentication
            if not self._session_db.check_token(session_token):
                raise Exception("Session token is invalid.")

            members = self._members_api.get_all_members()
            self._send_message(members, "all_members_response")
        except Exception:
            self._send_message(str(MemberResponse.FAILED), "all_members_response")

    def _handle_delete_member(self, payload):
        try:
            payload_parsed = json.loads(payload)
            member_id = payload_parsed['value']
            session_token = payload_parsed['session_token']
            # check authentication
            if not self._session_db.check_token(session_token):
                raise Exception("Session token is invalid.")

            self._members_api.delete_member(member_id)
            self._send_message(str(DeleteCodes.OK), "delete_response")
        except Exception:
            self._send_message(str(DeleteCodes.FAILED), "delete_response")

    def _handle_rfid(self, payload):
        pass