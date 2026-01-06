from abc import ABC


class Account(ABC):
    account_id = 0
    account_roles = dict()

    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        self.status = kwargs["status"]
        self.observer = kwargs["observer"]
        Account.account_id += 1
        self.id = Account.account_id

    @classmethod
    async def create(cls, **kwargs):
        obj = cls(**kwargs)
        observer = kwargs["observer"]
        await observer.notify(value=kwargs["name"], field="name", obj=obj)
        await observer.notify(value=kwargs["status"], field="status", obj=obj)
        return obj

    async def add_user_admin(self, admin):
        await self.observer.notify(self, "admins", admin)

    async def add_wallet(self, wallet):
        await self.observer.notify(self, "wallet", wallet)

    async def add_user(self, user):
        await self.observer.notify(self, "users", user)

    async def add_subscription(self, subscription):
        await self.observer.notify(self, "subscriptions", subscription)

    def get_id(self):
        return self.id


class NaturalAccount(Account):
    def __init__(self, name, status):
        super().__init__(name, status)
