from pydantic import BaseModel, EmailStr

class UserShema(BaseModel):
    name: str
    age: int


class USEResponse(BaseModel):
    id: int
    name: str
    age: int




