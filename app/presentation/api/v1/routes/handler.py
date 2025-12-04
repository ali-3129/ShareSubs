from fastapi import APIRouter, Depends, status, BackgroundTasks, Request
from ..shema.user_shema import UserShema, USEResponse
from ..dependencies.user_handler import service
router = APIRouter(prefix="/users" ,tags=["user"])

@router.post("/create", response_model=USEResponse, status_code = status.HTTP_201_CREATED)
async def user_handler(body: UserShema, bg:BackgroundTasks, user_handler = Depends(service)):

    user = await user_handler.user_create_handler(body)
    bg.add_task(user_handler.user_observer, body)
    return user 

@router.get("/{user_id}", response_model=USEResponse, status_code=status.HTTP_200_OK)
async def get_user(request: Request, user_id:int, service = Depends(service)):
    return await service.get_user_handler(user_id, request)

@router.get("/all_users")
async def get_all_user(limit: int = 10, offset: int =0, user_service= Depends()):
    pass