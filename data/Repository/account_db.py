from .db import Db
from infrastructure import container

class AccountDb(Db):

    @staticmethod
    def get_branch():
        return "Account"
    @staticmethod
    def shema():

        return {
            "name": None,
            "status": None,
            "wallet": None,
            "users": [],
            "admins": [],
            "subscriptions": []
    }


account_db = container.get_singleton(AccountDb)
