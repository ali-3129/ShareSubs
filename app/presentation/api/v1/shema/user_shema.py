from pydantic import BaseModel, ConfigDict, EmailStr

class UserShema(BaseModel):
    name: str
    age: int


class USEResponse(BaseModel):
    id: int
    user_name: str
    age: int
    model_config = ConfigDict(from_attributes=True)



