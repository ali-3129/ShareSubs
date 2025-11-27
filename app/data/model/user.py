
class User:
    user_id = 0

    def __init__(self, **kwargs):
        self.user_name = kwargs["name"]
        self.age = kwargs["age"]
        User.user_id += 1
        self.id = User.user_id
        self.observer = kwargs["observer"]
    
    @classmethod
    async def create(cls, **kwargs):
        obj = cls(**kwargs)
        observer = kwargs["observer"]
        await observer.notify(obj, "name", kwargs["name"])
        await observer.notify(obj, "age", kwargs["age"])
        return obj
    

    async def create_account(self, account):
        await self.observer.notify(self, "account", account)
    
    async def add_role(self, role):
        await self.observer.notify(self, "roles", role)
    
    def get_id(self):
        return self.id


class Role:
    role_id = 0

    def __init__(self, **kwargs):
        Role.role_id += 1
        self.id = Role.role_id
        self.name = kwargs["name"]
        self.role = kwargs["role"]
        self.observer = kwargs["observer"]

    @classmethod
    async def create(cls, **kwargs):
        obj = cls(**kwargs)
        observer = kwargs["observer"]
        await observer.notify(obj, "name", kwargs["name"])
        await observer.notify(obj, "role", kwargs["role"])
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
