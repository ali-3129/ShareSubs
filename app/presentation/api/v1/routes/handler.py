from uuid import uuid4
from fastapi import APIRouter, Depends, status, BackgroundTasks, Request, Cookie, Response
from ..shema.user_shema import UserShema, USEResponse, UserDbResponse, UserUpdateRes, Res
from ..dependencies.user_handler import service, current_user
from ..shema.account_shema import AccountResponse, AccountShema

router = APIRouter(prefix="/users", tags=["user"])


@router.post("/create", response_model=USEResponse, status_code=status.HTTP_201_CREATED)
async def user_handler(body: UserShema, bg: BackgroundTasks, user_handler=Depends(service)):
    user = await user_handler.user_create_handler(body)
    bg.add_task(user_handler.user_observer, body)
    return user


@router.post("/create_account", status_code=status.HTTP_201_CREATED)
async def create_account(body: AccountShema, service=Depends(service)):
    account = await service.create_account(body)
    return account


@router.post("delete/{user_id}")
async def delete_from_db(user_id, service=Depends(service)):
    res = await service.delete_from_db(user_id)
    return res


@router.post("db/update/{user_id}", response_model=Res)
async def user_update(user_id: int, body: UserUpdateRes, service=Depends(service)):
    return await service.name_update(user_id, body)


@router.get("/me")
async def me(service=Depends(current_user)):
    print(service)


@router.get("db/{user_id}", response_model=UserDbResponse, status_code=status.HTTP_200_OK)
async def get_user_from_db(request: Request, user_id: int, service=Depends(service)):
    return await service.get_user_from_db(user_id, request)


@router.get("/{user_id}", response_model=USEResponse, status_code=status.HTTP_200_OK)
async def get_user(request: Request, user_id: int, service=Depends(service)):
    return await service.get_user_handler(user_id, request)


@router.get("/db/all_users")
async def get_all_user(service =Depends(service)):
    users = await service.get_all_users()
    return users


@router.post("/logup")
async def login(response: Response):
    session_id = str(uuid4())
    response.set_cookie("sid", session_id)

    return {"status": True}


@router.post("/logout")
async def logout(response: Response, session_id: str | None = Cookie(default=None, alias="sid")):
    if session_id is None:
        print("raise")
    response.delete_cookie("sid")
    return {"status": True}
