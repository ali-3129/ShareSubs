from .db import Db
from infrastructure.bootstrap import container, account_observer

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
account_observer.attach(account_db)
