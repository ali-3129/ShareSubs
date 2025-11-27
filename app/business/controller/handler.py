from abc import ABC


class Handler(ABC):
    pass

class UserHandler(Handler):
    def __init__(self, **kwargs):
        self.service = kwargs["service"]
        self.user = kwargs["user"]

    def handle_account(self, name, status):
        user_service = self.service.create_account(name, status)
        return user_service
    
    def get_user_id(self):
        return self.user.get_id()
