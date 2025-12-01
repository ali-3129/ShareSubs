from ..shema.user_shema import UserShema, USEResponse
from business.model.factories import UserFactory
from business.controller.admin import UserAdmin
from fastapi import HTTPException, status

def service():
    user_service = UserHandler()
    return user_service

class UserHandler:

    async def user_create_handler(self, body:UserShema):
        user = UserFactory(name=body.name, age=body.age)
        a = await user.create()
        print(body.name)
        print(body.age)
        id = a.get_user_id()
        print(id)

        return a.get_user()
    

    @staticmethod
    async def user_observer(body):
        print(f"{body.name} is created")

    @staticmethod
    async def get_user_handler(user_id:int):
        from data.Repository.db import db
        res =  await db.get_user_by_id(user_id)
        if res is None:
            from infrastructure.common import raise_error
            raise_error("User not Founded", 404, "user faild")
            # raise HTTPException(
            #     status_code=status.HTTP_404_NOT_FOUND,
            #     detail={
            #         "erorr_code": 404,
            #         "message": "user not found"
            #     }
            # )
        else:
            id = user_id
            return {
                "id": id,
                "user_name": res["name"],
                "age": res["age"]
            }