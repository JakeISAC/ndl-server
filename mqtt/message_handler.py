import json
import uuid

from api.controller_api import ControllerApi
from api.members_api import MembersApi
from api.user_api import UserApi
from database.session_db import DbOperationsSession
from domains.member import Member
from domains.user import User
from logs.logs import Logs
from util.codes.authorization_codes import AuthorizationStatus
from util.codes.controller_codes import ControllerEvents
from util.codes.delete_codes import DeleteCodes as DeleteCodes
from util.codes.member_codes import AddMemberCodes as MemberResponse
from util.codes.user_codes import UserLoginCodes as UserCodes
from util.endpoints import Endpoints


class MessageHandler:
    def __init__(self, send_message):
        self._endpoints = Endpoints()
        self._logger = Logs().get_logger()
        self._user_api = UserApi()
        self._members_api = MembersApi()
        self._controller_api = ControllerApi()
        self._session_db = DbOperationsSession()
        self._send_message = send_message  # function
        # endpoints to user api
        self._login = "login_ask"
        self._register = "register"
        self._change_password = "change_password"
        self._add_member = "add_member"
        self._lock_status = "lock_status"
        self._last_active_person = "last_active_person"  # DONE in the Security module
        self._change_password = "change_password"
        self._all_members = "all_members"
        self._change_member = "change_member_data"
        self._delete_member = "delete_member"
        self._edit_member = "edit_member_status"
        # endpoint controller
        self._magnetic_lock = "magnetic_lock"  # publisher
        self._logs = "logs"  # subscriber
        self._lock = "lock"
        self._rfid = "rfid"

    def on_message(self, _, userdata, msg):
        payload = msg.payload.decode()
        match msg.topic:
            case self._login:
                self._handle_user_login(payload)
            case self._register:
                self._handle_user_register(payload)
            case self._change_password:
                self._handle_change_password(payload)
            case self._add_member:
                self._handle_add_member(payload)
            case self._all_members:
                self._handle_all_members(payload)
            case self._delete_member:
                self._handle_delete_member(payload)
            case self._rfid:
                self._handle_rfid(payload)
            case self._edit_member:
                self._handle_edit_member_status(payload)
            case _:
                pass

    def _handle_user_login(self, payload):
        try:
            user_data = User.extract_user(str(payload))
            token = self._user_api.login(user_data)
            response = {'code': str(UserCodes.FAILED), 'session_token': None}
            if token:
                response['code'] = str(UserCodes.OK)
                response['session_token'] = token
                self._logger.success("Successfully logged in")
                self._send_message(json.dumps(response), "login_response")
            else:
                self._logger.warning("Token is invalid")
                self._send_message(json.dumps(response), "login_response")
        except Exception as e:
            self._logger.exception(f"Failed to login: {e}")
            response = {'code': str(UserCodes.FAILED), 'session_token': None}
            self._send_message(json.dumps(response), "login_response")

    def _handle_user_register(self, payload):
        try:
            payload_parsed = json.loads(payload)
            user = payload_parsed['value']
            session_token = payload_parsed['session_token']
            # check authentication
            if not self._session_db.check_token(session_token):
                raise Exception("Session token is invalid.")

            user_data = User.extract_user(str(user))
            if not user_data:
                raise Exception("No user extracted")

            if self._user_api.register(user_data):
                self._logger.success(f"Successfully registered new user {user}")
                self._send_message(str(UserCodes.OK), "register_response")
            else:
                self._logger.warning(f"Failed to register a new user {user}")
                self._send_message(str(UserCodes.FAILED), "register_response")
        except Exception as e:
            self._logger.exception(f"Failed to register a new user: {e}")
            self._send_message(str(UserCodes.FAILED), "register_response")

    def _handle_change_password(self, payload):
        try:
            payload_parsed = json.loads(payload)
            username = payload_parsed['value']['username']
            old_password = payload_parsed['value']['old_password']
            new_password = payload_parsed['value']['new_password']
            session_token = payload_parsed['session_token']
            # check authentication
            if not self._session_db.check_token(session_token):
                raise Exception("Session token is invalid.")

            if self._user_api.change_password(username, old_password, new_password):
                self._logger.success(f"Successfully changed password for user {username}")
                self._send_message(str(UserCodes.OK), "change_password/response")
            else:
                self._logger.warning(f"Failed to change password for user {username}")
                self._send_message(str(UserCodes.FAILED), "change_password/response")
        except Exception as e:
            self._logger.exception(f"Failed to change password for user: {e}")
            self._send_message(str(UserCodes.FAILED), "change_password/response")

    def _handle_add_member(self, payload):
        try:
            payload_parsed = json.loads(payload)
            member = payload_parsed['value']
            session_token = payload_parsed['session_token']
            # check authentication
            if self._session_db.check_token(session_token):
                raise Exception("Session token is invalid.")

            member_extracted = Member.extract_member(member)
            if not member_extracted:
                raise Exception(f"No member extracted")

            if self._members_api.add_member(member_extracted):
                self._logger.success(f"Successfully added a new member {member}")
                self._send_message(str(MemberResponse.OK), "add_member_response")
            else:
                self._logger.warning(f"Failed to add a new member {member}")
                self._send_message(str(MemberResponse.FAILED), "add_member_response")
        except Exception as e:
            self._logger.exception(f"Failed to add a new member: {e}")
            self._send_message(str(MemberResponse.FAILED), "add_member_response")

    def _handle_all_members(self, payload):
        try:
            payload_parsed = json.loads(payload)
            session_token = payload_parsed['session_token']
            # check authentication
            if not self._session_db.check_token(session_token):
                raise Exception("Session token is invalid.")

            members = self._members_api.get_all_members()
            if members:
                self._logger.success("Successfully retrieved all members")
                self._send_message(members, "all_members_response")
            else:
                self._logger.warning("Failed to retrieved all members")
                self._send_message(str(MemberResponse.FAILED), "all_members_response")
        except Exception as e:
            self._logger.exception(f"Failed to retrieved all members: {e}")
            self._send_message(str(MemberResponse.FAILED), "all_members_response")

    def _handle_delete_member(self, payload):
        try:
            payload_parsed = json.loads(payload)
            member_id = uuid.UUID(payload_parsed['value'])
            session_token = payload_parsed['session_token']
            # check authentication
            if not self._session_db.check_token(session_token):
                raise Exception("Session token is invalid.")

            if self._members_api.delete_member(member_id):
                self._logger.success(f"Successfully deleted a member with ID: {member_id}")
                self._send_message(str(DeleteCodes.OK), "delete_response")
            else:
                self._logger.warning(f"Failed to delete a member with ID: {member_id}")
                self._send_message(str(DeleteCodes.FAILED), "delete_response")
        except Exception as e:
            self._logger.exception(f"Failed to delete a member: {e}")
            self._send_message(str(DeleteCodes.FAILED), "delete_response")

    def _handle_edit_member_status(self, payload):
        try:
            payload_parsed = json.loads(payload)
            session_token = payload_parsed['session_token']
            member_id = payload_parsed['value']['id']
            new_status = AuthorizationStatus.from_string(payload_parsed['value']['new_status'])
            # check authentication
            if not self._session_db.check_token(session_token):
                raise Exception("Session token is invalid.")

            if self._members_api.update_status(new_status, member_id):
                self._logger.success("Successfully updated a status of a member")
                self._send_message(str(MemberResponse.OK), "edit_member_status/response")
            else:
                self._logger.warning("Failed to update a status of a member")
                self._send_message(str(MemberResponse.FAILED), "edit_member_status/response")
        except Exception as e:
            self._logger.exception(f"Failed to edit member status: {e}")
            self._send_message(str(MemberResponse.FAILED), "edit_member_status/response")

    def _handle_rfid(self, payload):
        try:
            uid = str(payload)
            if self._controller_api.rfid_check(uid):
                self._logger.success(f"Successfully logged in with the RFID: {uid}")
                self._send_message(str(ControllerEvents.OPEN_LOCK), "magnetic_lock")
            else:
                self._logger.warning(f"Failed to logged in with the RFID: {uid}")
                self._send_message(str(ControllerEvents.CLOSE_LOCK), "magnetic_lock")
        except Exception as e:
            self._logger.exception(f"Failed to logged in with RFID: {e}")
            self._send_message(str(ControllerEvents.CLOSE_LOCK), "magnetic_lock")