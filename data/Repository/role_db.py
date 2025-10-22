from .db import Db
from infrastructure import container
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
