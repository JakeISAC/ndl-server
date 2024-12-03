from database.members_db import DbOperationsMembers


class MembersApi:
    def __init__(self):
        self._db_access = DbOperationsMembers()

    def update_status(self):
        pass