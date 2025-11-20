from db import Db

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