
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserShema(BaseModel):
    name: str
    age: int = Field(ge=18)


class USEResponse(BaseModel):
    id: int
    user_name: str
    age: int
    model_config = ConfigDict(from_attributes=True)


class UserDbResponse(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class UserUpdateRes(BaseModel):
    name: str


class Res(BaseModel):
    response: str


class LoginShema(BaseModel):
    username: EmailStr
    password: str
    role_name: str
    name: str


class TokenRes(BaseModel):
    sub: str
