from abc import ABC
from data.Repository.db import db

class Admin(ABC):
    @staticmethod
    async def get_by_id():
        pass

class UserAdmin(Admin):
    @staticmethod
    async def get_by_id(id):
       return await db.get_user_by_id(id)