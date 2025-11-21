from fastapi import APIRouter, Depends
from ..shema.user_shema import UserShema
from ..dependencies.user_handler import user_create_handler
router = APIRouter(prefix="/users" ,tags=["user"])

@router.post("/create")
async def user_handler(body: UserShema, user_handler = Depends(user_create_handler)):
    pass