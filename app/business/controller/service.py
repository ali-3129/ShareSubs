from abc import ABC
from app.business import AdminUserAccountFactory


class Service(ABC):
    def __init__(self, instance):
        self.instance = instance
    @staticmethod
    def delete(cls, instance, user):
        pass


class UserService(Service):

    def __init__(self, **kwargs):
        self.user = kwargs["user"]
        super().__init__(self.user)

    @staticmethod
    def delete(cls, instance, user):
        pass

    def create_account(self, **kwargs):
        user_account = AdminUserAccountFactory(user=self.user, name=kwargs["name"], status=kwargs["status"])
        return user_account