from ..shema.user_shema import UserShema, USEResponse
from business.model.factories import UserFactory
from business.controller.admin import UserAdmin
from data.Repository.db import db


async def user_create_handler(body:UserShema):
    user = UserFactory(name=body.name, age=body.age)
    a = await user.create()
    print(body.name)
    print(body.age)
    id = a.get_user_id()
    print(id)

    return USEResponse(id=id, name=body.name, age=body.age)


async def get_user_handler(user_id:int):
   db.get_data()