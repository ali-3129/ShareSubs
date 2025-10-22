
from business.controller.manager import AccountFactory
from infrastructure import container

class User:
    user_id = 0

    def __init__(self, name, age, observer):
        self.user_name = name
        self.age = age
        self.id = User.user_id + 1
        self.observer = observer
    
    @classmethod
    async def create(cls, name, age, observer):
        obj = cls(name, age)
        await observer.notify(obj, "name", name)
        await observer.notify(obj, "age", age)
        return obj
    

    async def create_account(self, name, status):
        account = await container.get_factory(AccountFactory, user=self, name=name, status=status)
        return account
    
    async def add_role(self, role):
        await self.observer.notify(self, "roles", role)
    
    async def add_account(self, account):
        await self.observer.notify(self, "accounts", account)

    def get_id(self):
        return self.id


class Role:
    role_id = 0

    def __init__(self, name, role, observer):
        Role.role_id += 1
        self.id = Role.role_id
        self.name = name
        self.role = role
        self.observer = observer

    @classmethod
    async def create(cls, name, role, observer):
        obj = cls(name, role)
        await observer.notify(obj, "name", name)
        await observer.notify(obj, "role", role)
        return obj

    async def add_option(self, option, quantity):
        await self.observer.notify(self, "options", option)
        await self.observer.notify(self, "quantitys", quantity)

    def get_id(self):
        return self.id
    
    async def change_to_admin(self):
        await self.observer.notify(self, "role", "admin")


class SendOption:
    def __init__(self):
        pass


class ReciveOption:
    pass


class AddOption:
    pass


class Subtract:
    pass
