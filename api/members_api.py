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
            return self._db_access.upload_to_db(member)
        except Exception as e:
            return False

    def remove_member(self, user_id):
        try:
            return self._db_access.remove(user_id)
        except Exception as e:
            return False

    def update_status(self, new_status):
        pass

    def list_members_with_status(self):
        pass