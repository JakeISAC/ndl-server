import json
from typing import List

from database.members_db import DbOperationsMembers
from domains.member import Member
from face_recognition_util.encode_faces import EncodeFaces
from logs.logs import Logs


class MembersApi:
    def __init__(self):
        self._logger = Logs().get_logger()
        self._db_access = DbOperationsMembers()

    def add_member(self, member: Member):
        self._logger.trace("Attempting to add a member")
        try:
            # encode faces of people
            new_encode = EncodeFaces(member.images_path)
            encode = new_encode.generate_encodings_from_file()
            if not encode:
                raise Exception("The encode is None")

            member.face_encodings = encode
            return self._db_access.upload(member)
        except Exception as e:
            self._logger.exception(f"{e}")
            return None

    def delete_member(self, member_id):
        self._logger.trace("Attempting to delete a member")
        try:
            return self._db_access.remove(member_id)
        except Exception as e:
            self._logger.exception(f"{e}")
            return None

    def update_status(self, member_id, new_status, date=None):
        self._logger.trace("Attempting to update member status")
        try:
            return self._db_access.update_status(new_status, member_id, date)
        except Exception as e:
            self._logger.exception(f"{e}")
            return None

    def list_members_with_authorization(self, authorization):
        self._logger.trace("Attempting to list all members given authorization")
        try:
            members = self._db_access.search_authorization(authorization)
            return self._members_array_json(members)
        except Exception as e:
            self._logger.exception(f"{e}")
            return None

    def get_all_members(self):
        self._logger.trace("Attempting to list all members")
        try:
            members = self._db_access.get_all()
            return self._members_array_json(members)
        except Exception as e:
            self._logger.exception(f"{e}")
            return None

    @classmethod
    def _members_array_json(cls, members: List[Member]):
        logger = Logs().get_logger()
        logger.trace("Attempting to deserialize an array of JSON objects to Members array")
        try:
            json_data = []
            for member in members:
                json_data.append(member.to_dict())
            return json.dumps(json_data)
        except Exception as e:
            logger.exception(f"Failed to create an array of Members from JSON list: {e}")
            return None
