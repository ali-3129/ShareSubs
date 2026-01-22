from sqlalchemy import table, Table, column, Column
from sqlalchemy import ForeignKey
from app.data.Repository.db import Db, Base

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


user_account = Table(
    "user_account",
    Base.metadata,
    Column("User_id", ForeignKey("users.id"), primary_key=True),
    Column("account_id", ForeignKey("accounts.id"), primary_key=True)

)
