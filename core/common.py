import asyncio
from abc import ABC, abstractmethod


class Db(ABC):
    db = {"Account": {}, "User": {}, "Role": {}, "UserRole": {}, "UserAccount": {}}

    @staticmethod
    def shema():
        pass
    @staticmethod
    def get_branch():
        pass

    async def update(self, obj, field, value):
        id = obj.get_id()
        if id not in Db.db[self.get_branch()]:
            Db.db[self.get_branch()][id] = self.shema()
        if field in Db.db[self.get_branch()][id] and isinstance(Db.db[self.get_branch()][id][field], list):
                Db.db[self.get_branch()][id][field].append(value)
        else:
                print(field)
                Db.db[self.get_branch()][id][field] = value

    def get_data(self):
        print(f"\n{self.db}\n")


class Logger:
    async def update(self, obj, field, value):
        print(f"value {value} in {field} added")


class Observer:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    async def notify(self, obj, field, value):
        for observer in self.observers:
            
            await observer.update(obj, field, value)


class AccountDb(Db):

    @staticmethod
    def get_branch():
        return "Account"
    @staticmethod
    def shema():

        return {
            "name": None,
            "status": None,
            "wallet": None,
            "users": [],
            "admins": [],
            "subscriptions": []
    }



class UserDb(Db):

    @staticmethod
    def get_branch():
        return "User"

    @staticmethod
    def shema():
        return {
            "name": None,
            "age": None,
            "role": None,
            "roles": [],
            "accounts": [],
    }


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
    

class UserAccountDb(Db):

    @staticmethod
    def get_branch():
        return "User_Account_Db"
    
    @staticmethod
    def shema():
        return {
            "user": None,
            "account": None
        }

db = AccountDb()
observer = Observer()
logger = Logger()
observer.attach(logger)
observer.attach(db)

user_logger = Logger()
user_db = UserDb()
user_observer = Observer()
user_observer.attach(user_db)
user_observer.attach(user_logger)

user_role_db = UserRollDb()
user_role_observer = Observer()
user_role_observer.attach(user_role_db)
user_role_logger = Logger()
user_role_observer.attach(user_role_logger)

role_logger = Logger()
role_db = RoleDb()
role_observer = Observer()
role_observer.attach(role_db)
role_observer.attach(role_logger)