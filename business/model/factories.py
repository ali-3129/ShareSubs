from infrastructure.bootstrap import container
from data.Repository.account_db import account_observer
from data.Repository.user_db import user_observer
from business import Account
from infrastructure.bootstrap import container, user_role_observer, role_observer
from data.model.account import Account
from data.model.user import User, Role
from business.controller.service import UserService
from business.controller.handler import UserHandler
from abc import ABC
import asyncio


class Factory(ABC):

    @staticmethod
    def create():
        pass


class AccountFactory(Factory):

    @staticmethod
    async def create(name, status):
        account = await container.get_factory(Account, name=name, status=status, observer=account_observer)
        return account


class UserFactory(Factory):

    @staticmethod
    async def create(name, age):
        user = await container.get_factory(User, name=name, age=age, observer=user_observer)
        service = container.get_factory(UserService, user=user)
        handler = container.get_factory(UserHandler, service=service)
        return handler
    

class RoleFactory(Factory):

    @staticmethod
    async def create(name, role):
        role = await container.get_factory(Role, name=name, role=role, observer=role_observer)
        return role


class AdminUserAccountFactory(Factory):
    @staticmethod
    async def create(**kwargs):
        user = kwargs["user"]
        account = await AccountFactory.create(**kwargs)
        user.create_account(account)
        role = await container.get_factory(Role, role="admin", name="owner")
        user_role = await container.get_factory(UserRole, role=role, user=kwargs["user"])
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