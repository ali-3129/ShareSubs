from .db import Db
from infrastructure.bootstrap import container, user_role_observer, role_observer
class RoleDb(Db):
    @staticmethod
    def get_branch():
        return "Role"
    
    @staticmethod
    def shema():
        return {
            "name": None,
            "options": [],
            "quantitys": []
        }
    
class UserRollDb(Db):
    @staticmethod
    def get_branch():
        return "UserRole"
    
    @staticmethod
    def shema():
        return{
            "user": None,
            "role": None
        }
    

user_role_db = container.get_singleton(UserRollDb)
role_db = container.get_singleton(RoleDb)
user_role_observer.attach(user_role_db)
role_observer.attach(role_db)

