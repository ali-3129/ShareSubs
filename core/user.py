from bootstrap.bootstrap import user_observer, role_observer, container
from core.manager import AccountFactory


class User:
    user_id = 0

    def __init__(self, name, age):
        self.user_name = name
        self.age = age
        self.id = User.user_id + 1
    
    @classmethod
    async def create(cls, name, age):
        obj = cls(name, age)
        await user_observer.notify(obj, "name", name)
        await user_observer.notify(obj, "age", age)
        return obj
    

    async def create_account(self, name, status):
        account = await container.get_factory(AccountFactory, user=self, name=name, status=status)
        return account
    
    async def add_role(self, role):
        await user_observer.notify(self, "roles", role)
    
    async def add_account(self, account):
        await user_observer.notify(self, "accounts", account)

    def get_id(self):
        return self.id


class Role:
    role_id = 0

    def __init__(self, name, role):
        Role.role_id += 1
        self.id = Role.role_id
        self.name = name
        self.role = role

    @classmethod
    async def create(cls, name, role):
        obj = cls(name, role)
        await role_observer.notify(obj, "name", name)
        await role_observer.notify(obj, "role", role)
        return obj

    async def add_option(self, option, quantity):
        await role_observer.notify(self, "options", option)
        await role_observer.notify(self, "quantitys", quantity)

    def get_id(self):
        return self.id
    
    async def change_to_admin(self):
        await role_observer.notify(self, "role", "admin")


class SendOption:
    def __init__(self):
        pass


class ReciveOption:
    pass


class AddOption:
    pass


class Subtract:
    pass
