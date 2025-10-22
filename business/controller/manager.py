from business import Account
from business import user_role_observer, container

class AccountFactory:
    def __init__(self, name, status, user):
        self.name = name
        self.status = status
        self.user = user

    @staticmethod
    async def create(**kwargs):
        
        account = await container.get_factory(Account, **kwargs)
        user_role = await container.get_factory(UserRole, role="public", user=kwargs["user"])
        await account.add_user_admin(user_role)
        admin_user_account = await container.get_factory(AdminUserAccount, role_user=user_role, account=account, user=kwargs["user"])
        return admin_user_account




class UserRole:
    user_role_id = 0
    def __init__(self, **kwargs):
        UserRole.user_role_id += 1
        self.role = kwargs["role"]
        self.user = kwargs["user"]
        
    @classmethod
    async def create(cls, **kwargs):
        obj = cls(**kwargs)
        await user_role_observer.notify(obj, "role", kwargs["role"])
        await user_role_observer.notify(obj, "user", kwargs["user"])
        return obj
    
    def get_id(self):
        return self.user_role_id




class UserAccount:
    pass


class AdminUserAccount:
    aua_id = 0
    def __init__(self, **kwargs):
        self.user_role = kwargs["role_user"]
        self.account = kwargs["account"]
        self.user = kwargs["user"]
        AdminUserAccount.aua_id += 1
        self.id = self.aua_id

    @classmethod
    async def create(cls, **kwargs):
        obj = cls(**kwargs)

        return obj