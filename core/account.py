from abc import ABC, abstractmethod
from bootstrap.bootstrap import account_observer


class Account(ABC):
    account_id = 0
    account_roles = dict()

    def __init__(self, name, status, user):
        self.name = name
        self.status = status
        Account.account_id += 1
        self.id = Account.account_id

    @classmethod
    async def create(cls, name, status):
        obj = cls(name, status)
        await account_observer.notify(value=name, field="name", obj=obj)
        await account_observer.notify(value=status, field="status", obj=obj)
        return obj
    async def add_user_admin(self, admin):
        await account_observer.notify(self, "admins", admin)

    async def add_wallet(self, wallet):
        await account_observer.notify(self, "wallet", wallet)

    async def add_user(self, user):
        await account_observer.notify(self, "users", user)

    async def add_subscription(self, subscription):
        await account_observer.notify(self, "subscriptions", subscription)

    def get_id(self):
        return self.id


class NaturalAccount(Account):
    def __init__(self, name, status):
        super().__init__(name, status)