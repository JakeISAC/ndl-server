import json
from typing import List

from database.members_db import DbOperationsMembers
from domains.member import Member
from face_recognition_util.encode_faces import EncodeFaces


class MembersApi:
    def __init__(self):
        self._db_access = DbOperationsMembers()

    def add_member(self, member: Member):
        try:
            # encode faces of people
            new_encode = EncodeFaces(member.images_path)
            encode = new_encode.generate_encodings_from_file()
            member.face_encodings = encode
            return self._db_access.upload(member)
        except Exception as e:
            return None

    def delete_member(self, member_id):
        try:
            return self._db_access.remove(member_id)
        except Exception as e:
            return None

    def update_status(self, new_status, member_id):
        try:
            return self._db_access.update_status(new_status, member_id)
        except Exception as e:
            return None

    def list_members_with_authorization(self, authorization):
        try:
            members = self._db_access.search_authorization(authorization)
            return self._members_array_json(members)
        except Exception as e:
            return None

    def get_all_members(self):
        try:
            members = self._db_access.get_all()
            return self._members_array_json(members)
        except Exception as e:
            return None

    @classmethod
    def _members_array_json(cls, members: List[Member]):
        try:
            json_data = []
            for member in members:
                json_data.append(member.to_dict())
            return json.dumps(json_data)
        except Exception as e:
            return None
