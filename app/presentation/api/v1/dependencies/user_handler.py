from data.Repository.account_db import AccountModel
from ..shema.user_shema import UserShema, USEResponse
from business.model.factories import UserFactory
from business.controller.admin import UserAdmin
from fastapi import HTTPException, status, Request, Cookie, Depends
from .sesstion import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from data.Repository.user_db import UserModel
from sqlalchemy import select, delete, update
from sqlalchemy.orm import selectinload


def service(session: AsyncSession = Depends(get_session)):
    user_service = UserHandler(session)
    return user_service


class UserHandler:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def user_create_handler(self, body: UserShema):
        user = UserFactory(name=body.name, age=body.age)
        a = await user.create()
        print(body.name)
        print(body.age)
        id = a.get_user_id()
        print(id)
        user_model = UserModel(name=body.name, role_name="admin")
        self.session.add(user_model)
        await self.session.commit()

        user = a.get_user()
        return user

    async def create_account(self, body):
        account = AccountModel(name=body.name)
        res = (await self.session.execute(select(UserModel)
                                          .where(UserModel.id == 1).
                                          options(selectinload(UserModel.accounts)))).scalar_one()

        self.session.add(account)
        account.users.append(res)
        await self.session.commit()
        print(account.users[0].name)

    @staticmethod
    async def user_observer(body):
        print(f"{body.name} is created")

    async def get_user_from_db(self, id: int, request):

        try:
            result = await self.session.execute(select(UserModel.id, UserModel.name).where(UserModel.id == id))
            user = result.mappings().first()
            if user is None:
                from infrastructure.common import raise_error
                raise_error(request, "User not Founded", 404, "user faild")
        except:
            await self.session.rollback()
        return user

    async def name_update(self, id: int, body):
        await self.session.execute(update(UserModel).where(UserModel.id == id).values(name=body.name))
        await self.session.commit()
        return {"response": "ok"}

    async def delete_from_db(self, user_id):
        await self.session.execute(delete(UserModel).where(UserModel.id == user_id))
        await self.session.commit()
        return {"response": "ok"}

    async def get_user_handler(self, user_id: int, request: Request):
        from data.Repository.db import db
        res = await db.get_user_by_id(user_id)
        if res is None:
            from infrastructure.common import raise_error
            raise_error(request, "User not Founded", 404, "user faild")

        else:
            id = user_id
            result = await self.session.execute(select(UserModel.id).where(UserModel.id == id))
            print(result)
            return {
                "id": id,
                "user_name": res["name"],
                "age": res["age"]
            }

    async def get_all_users(self):
        res = await self.session.execute(select(UserModel)
                                         .offset(0).limit(10)
                                         .options(selectinload(UserModel.accounts)))
        users = res.scalars().all()

        return users


async def current_user(sid: str | None = Cookie(default=None, alias="sid")):
    if sid is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    return sid
