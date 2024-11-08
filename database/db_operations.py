from cassandra.cluster import Cluster

from util.endpoints import Endpoints
import pickle
from datetime import datetime

from util.program_codes import AuthorizationStatus


class DatabaseOperations:
    def __init__(self):
        self._cluster = Cluster()
        self._session = self._cluster.connect()
        self._endpoints = Endpoints()
        self._session.set_keyspace(self._endpoints.KEYSPACE)

    def upload_to_db(self, person: object):
        query_str = (f"INSERT INTO {self._endpoints.USER_TABLE} (id, authorization_status, access_remaining_date_time, name, path_to_images, face_encodings) "
                     f"VALUES (?, ?, ?, ?, ?, ?)")
        query = self._session.prepare(query_str)
        encoded_face_encodings = pickle.dumps(person.face_encodings)
        self._session.execute(query, [person.id, person.authorization.value, person.access_remaining_date_time,
                                      person.name, person.images_path, encoded_face_encodings])

    """
        TODO: rewrite the function to be more interactive and allow search over: name, id, authorization.
                Remember to add ALLOW FILTERING at the end since, id and authorization not part of primary key. 
        
        In general I will have to redesign the DB schema for this. For now it can stay as is. 
    """
    def search(self, face_encodings=None, name=None):
        try:
            found = []
            if face_encodings and not name:
                encoded_face_encodings = pickle.dumps(face_encodings)
                query = f"SELECT * FROM {self._endpoints.USER_TABLE} WHERE face_encodings=?"
                prepared_query = self._session.prepare(query)
                for row in self._session.execute(prepared_query, [encoded_face_encodings]):
                    found.append(self._row_to_person(row))
            elif not face_encodings and name:
                query = f"SELECT * FROM {self._endpoints.USER_TABLE} WHERE name=?"
                prepared_query = self._session.prepare(query)
                for row in self._session.execute(prepared_query, [name]):
                    found.append(self._row_to_person(row))
            elif face_encodings and name:
                encoded_face_encodings = pickle.dumps(face_encodings)
                query = f"SELECT * FROM {self._endpoints.USER_TABLE} WHERE face_encodings=? AND name=?"
                prepared_query = self._session.prepare(query)
                for row in self._session.execute(prepared_query, [encoded_face_encodings, name]):
                    found.append(self._row_to_person(row))
            else:
                raise Exception("Search not possible no parameters provided.")

            return found

        except Exception as e:
            raise e

    def search_authorization(self, authorization=None):
        try:
            found = []
            if authorization:
                query = f"SELECT * FROM {self._endpoints.KEYSPACE}.{self._endpoints.USER_TABLE} WHERE authorization_status=? ALLOW FILTERING"
                prepared_query = self._session.prepare(query)
                for row in self._session.execute(prepared_query, [authorization]):
                    found.append(self._row_to_person(row))
            else:
                raise Exception("Search not possible no parameters provided.")

            return found

        except Exception as e:
            raise e



    def get_all(self):
        people = []
        query = f"SELECT * FROM {self._endpoints.KEYSPACE}.{self._endpoints.USER_TABLE}"
        prepared_query = self._session.prepare(query)
        for row in self._session.execute(prepared_query):
            people.append(self._row_to_person(row))
        return people

    @classmethod
    def _row_to_person(cls, row):
        from domains.people import Person

        try:
            face_encodings = pickle.loads(row.face_encodings)
            auth_status = AuthorizationStatus(row.authorization_status)

            return Person(id=row.id,
                          name=row.name,
                          images_path=row.path_to_images,
                          authorization=auth_status,
                          face_encodings=face_encodings,
                          access_remaining_date_time= row.access_remaining_date_time
                          )

        except Exception as e:
            raise e