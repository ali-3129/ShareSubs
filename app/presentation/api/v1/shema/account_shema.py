from pydantic import BaseModel


class AccountShema(BaseModel):
    id: int
    name: str


class AccountResponse(BaseModel):
    pass
