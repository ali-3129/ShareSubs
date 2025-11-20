from .db import Db
from infrastructure.bootstrap import container, user_observer

class UserDb(Db):

    @staticmethod
    def get_branch():
        return "User"

    @staticmethod
    def shema():
        return {
            "name": None,
            "age": None,
            "role": None,
            "roles": [],
            "accounts": [],
    }

user_db = container.get_singleton(UserDb)
user_observer.attach(user_db)

