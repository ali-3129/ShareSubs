from common import *
from User import *
from Account import *


class AccountFactory:
    def __init__(self, name, status, user):
        self.name = name
        self.status = status
        self.user = user


    async def create(self):
        account = await Account.create(self.name, self.status)
        user_role = await UserRole.create(self.user, "admin")
        await account.add_user_admin(user_role)
        admin_user_account = await AdminUserAccount.create(user_role, account)
        return admin_user_account




class UserRole:
    user_role_id = 0
    def __init__(self, user, role="public"):
        UserRole.user_role_id += 1
        self.role = role
        self.user = user
        
    @classmethod
    async def create(cls, user, role="public"):
        obj = cls(user, role="public")
        await user_role_observer.notify(obj, "role", role)
        await user_role_observer.notify(obj, "user", user)
        return obj
    
    def get_id(self):
        return self.user_role_id




class UserAccount:
    pass


class AdminUserAccount:
    aua_id = 0
    def __init__(self, user_role, account):
        self.user_role = user_role
        self.account = account
        AdminUserAccount.aua_id += 1
        self.id = self.aua_id

    @classmethod
    async def create(cls, user_role, account):
        obj = cls(user_role, account)

        return obj