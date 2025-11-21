from pydantic import BaseModel, EmailStr

class UserShema(BaseModel):
    name: str
    age: int