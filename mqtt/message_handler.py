import json
from api.user_api import UserApi
from api.members_api import MembersApi
from database.session_db import DbOperationsSession
from domains.member import Member
from util.endpoints import Endpoints
from util.program_codes import UserLoginResponse as UserCodes
from util.program_codes import AddMemberResponse as MemberResponse

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
        self._last_active_person = "last_active_person"
        self._change_password = "change_password"
        self._all_members = "all_members"
        self._change_member = "change_member_data"
        self._delete_member = "delete_member"
        # endpoint controller
        self._magnetic_lock = "magnetic_lock"  # publisher
        self._logs = "logs"  # subscriber

    def on_message(self, _, userdata, msg):
        match msg.topic:
            case self._logs:
                payload = msg.payload.decode()
                print(payload)
            case self._login:
                payload = msg.payload.decode()
                print(payload)
                token = self._user_api.login(str(payload))
                response = {'code': str(UserCodes.FAILED), 'session_token': None}
                if token:
                    response['code'] = str(UserCodes.OK)
                    response['session_token'] = token
                    self._send_message(json.dumps(response), "login_response")
                else:
                    self._send_message(json.dumps(response), "login_response")
            case self._register:
                payload = msg.payload.decode()
                print(payload)
                payload_parsed = json.loads(payload)
                user = payload_parsed['value']
                session_token = payload_parsed['session_token']
                if self._session_db.check_token(session_token):
                    if self._user_api.register(str(user)):
                        self._send_message(str(UserCodes.OK), "register_response")
                    else:
                        self._send_message(str(UserCodes.FAILED), "register_response")
                else:
                    self._send_message(str(UserCodes.FAILED), "register_response")
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
                    self._send_message(str(MemberResponse.OK), "add_member_response")
                else:
                    self._send_message(str(MemberResponse.FAILED), "add_member_response")
            case _:
                pass
