from ..shema.user_shema import UserShema, USEResponse
from business.model.factories import UserFactory
from business.controller.admin import UserAdmin
from fastapi import HTTPException, status, Request, Cookie, Depends
from .sesstion import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from data.Repository.user_db import UserModel
from sqlalchemy import select, delete

def service(session : AsyncSession = Depends(get_session)):
    user_service = UserHandler(session)
    return user_service

class UserHandler:
    def __init__(self, session : AsyncSession):
        self.session = session

    async def user_create_handler(self, body:UserShema ):
        user = UserFactory(name=body.name, age=body.age)
        a = await user.create()
        print(body.name)
        print(body.age)
        id = a.get_user_id()
        print(id)
        
        user = a.get_user()
        sec_user = UserModel(id=id)
        try:
            self.session.add(sec_user)
            await self.session.commit()
            await self.session.refresh(sec_user)
        except:
            del_op = self.session.get(UserModel, id)
            await self.session.delete(del_op)
            await self.session.commit()
        return user
    

    @staticmethod
    async def user_observer(body):
        print(f"{body.name} is created")

    
    async def get_user_handler(self, user_id:int, request:Request):
        from data.Repository.db import db
        res =  await db.get_user_by_id(user_id)
        if res is None:
            from infrastructure.common import raise_error
            raise_error(request, "User not Founded", 404, "user faild")
            
        else:
            id = user_id
            result = await self.session.execute(select(UserModel.id).where(UserModel.id==id))
            print(result)
            return {
                "id": id,
                "user_name": res["name"],
                "age": res["age"]
            }
    

async def current_user(sid : str | None = Cookie(default=None, alias="sid")):
    if sid is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    return sid