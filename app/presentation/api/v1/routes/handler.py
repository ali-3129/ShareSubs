from fastapi import APIRouter, Depends
from ..shema.user_shema import UserShema
from ..dependencies.user_handler import user_create_handler, get_user_handler
router = APIRouter(prefix="/users" ,tags=["user"])

@router.post("/create")
async def user_handler(body: UserShema, user_handler = Depends(user_create_handler)):
    print(user_handler)

@router.get("/{user_id}")
async def get_user(user_id:int, get_user_handler = Depends(get_user_handler)):
    return 

@router.get("/all_users")
async def get_all_user(limit: int = 10, offset: int =0, user_service= Depends()):
    pass