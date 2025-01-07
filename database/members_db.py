import pickle
import uuid

from cassandra.cluster import Cluster

from domains.member import Member
from logs.logs import Logs
from util.codes.authorization_codes import AuthorizationStatus
from util.endpoints import Endpoints


class DbOperationsMembers:
    def __init__(self):
        self._logger = Logs().get_logger()
        self._cluster = Cluster()
        self._session = self._connect()
        self._endpoints = Endpoints()
        self._session.set_keyspace(self._endpoints.KEYSPACE_MEMBER)

    def _connect(self):
        try:
            self._logger.info("Connecting to Members database")
            return self._cluster.connect()
        except Exception as e:
            self._logger.critical(f"Failed to connect to Members database: {e}")
            raise e

    def upload(self, member: Member):
        try:
            query_str = (
                f"INSERT INTO {self._endpoints.MEMBER_TABLE} (id, authorization_status, access_remaining_date_time, name, path_to_images, face_encodings) "
                f"VALUES (?, ?, ?, ?, ?, ?)")
            query = self._session.prepare(query_str)
            encoded_face_encodings = pickle.dumps(member.face_encodings)
            self._session.execute(query, [member.id, member.authorization.value, member.access_remaining_date_time,
                                          member.name, member.images_path, encoded_face_encodings])
            self._logger.debug(f"Uploaded {member.name} [{member.id}] with {str(member.authorization)}")
            return True
        except Exception as e:
            self._logger.exception(f"Failed to upload {member.name}: {e}")
            return None

    def delete(self, member_id: uuid.UUID):
        try:
            select_query = f"SELECT name FROM {self._endpoints.MEMBER_TABLE} WHERE id=? ALLOW FILTERING"
            prepared_query = self._session.prepare(select_query)
            rows_to_delete = self._session.execute(prepared_query, [member_id])

            for row in rows_to_delete:
                query_str = f"DELETE FROM {self._endpoints.MEMBER_TABLE} WHERE name=?"
                query = self._session.prepare(query_str)
                self._session.execute(query, [row.name])
                self._logger.debug(f"Removed {row.name}, {member_id}")
            return True
        except Exception as e:
            self._logger.exception(f"Failed to remove {member_id}: {e}")
            return None

    def update_status(self, member_id, new_status, date=None):
        try:
            select_query = f"SELECT name,path_to_images FROM {self._endpoints.MEMBER_TABLE} WHERE id=? ALLOW FILTERING"
            prepared_query = self._session.prepare(select_query)
            rows_to_update = self._session.execute(prepared_query, [member_id])

            if not rows_to_update:
                raise Exception(f"Member with id {member_id} not found.")

            if new_status == AuthorizationStatus.AUTHORIZED or new_status == AuthorizationStatus.NOT_AUTHORIZED:
                query_str = f"UPDATE {self._endpoints.MEMBER_TABLE} SET authorization_status=? WHERE name=? AND path_to_images=?"
            else:
                query_str = f"UPDATE {self._endpoints.MEMBER_TABLE} SET authorization_status=?, access_remaining_date_time=? WHERE name=? AND path_to_images=?"

            for row in rows_to_update:
                query = self._session.prepare(query_str)
                self._session.execute(query, [new_status.value, row.name,
                                              row.path_to_images]) if not date else self._session.execute(query, [
                    new_status.value, date, row.name, row.path_to_images])
                self._logger.debug(f"Updated {member_id} with {AuthorizationStatus.__str__(new_status)}")
            return True
        except Exception as e:
            self._logger.exception(f"Failed to update {member_id}: {e}")
            return None

    def search_authorization(self, authorization=None):
        try:
            if not authorization:
                raise Exception("Search not possible no parameters provided.")

            members = []
            query_str = f"SELECT * FROM {self._endpoints.MEMBER_TABLE} WHERE authorization_status=? ALLOW FILTERING"
            query = self._session.prepare(query_str)
            for row in self._session.execute(query, [authorization]):
                members.append(self._row_to_member(row))
            self._logger.debug(f"Found {len(members)} members")
            return members
        except Exception as e:
            self._logger.exception(f"Failed to find {authorization}: {e}")
            return None

    def get_all(self):
        try:
            members = []
            query_str = f"SELECT * FROM {self._endpoints.MEMBER_TABLE}"
            query = self._session.prepare(query_str)
            for row in self._session.execute(query):
                members.append(self._row_to_member(row))
            self._logger.debug(f"Found {len(members)} members")
            return members
        except Exception as e:
            self._logger.exception(f"Failed to retrieve members: {e}")
            return None

    def search_user(self, member_id):
        try:
            if not member_id:
                raise Exception("Member id not provided.")

            members = []
            query_str = f"SELECT * FROM {self._endpoints.MEMBER_TABLE} WHERE id=? ALLOW FILTERING"
            query = self._session.prepare(query_str)
            for row in self._session.execute(query, [member_id]):
                members.append(self._row_to_member(row))
            self._logger.debug(f"Found members with id {member_id}")
            return members
        except Exception as e:
            self._logger.exception(f"Failed to find {member_id}: {e}")
            return None

    @classmethod
    def _row_to_member(cls, row):
        try:
            if not row:
                raise Exception("Row is null")

            face_encodings = pickle.loads(row.face_encodings)
            auth_status = AuthorizationStatus(row.authorization_status)
            return Member(id=row.id,
                          name=row.name,
                          images_path=row.path_to_images,
                          authorization=auth_status,
                          face_encodings=face_encodings,
                          access_remaining_date_time=row.access_remaining_date_time
                          )
        except Exception as e:
            raise e
