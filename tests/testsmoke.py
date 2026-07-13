from unittest.mock import AsyncMock, MagicMock

import anyio
from fastapi import HTTPException
from pydantic import ValidationError
import pytest
from app.presentation.api.v1.dependencies.user_handler import service, UserHandler
from app.presentation.api.v1.shema.user_shema import UserShema
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.Repository.user_db import UserModel
@pytest.fixture
def mock():
    def mocker():
        return MagicMock(spec= AsyncSession)
    return mocker

def user_shema(name, age):
    shema = UserShema(name=name, age=age)
    return shema

def test_smoke():
    assert 1 + 1 == 2

class Session:
    def __init__(self):
        self.user = []
        self.commit = AsyncMock()

    def add(self, user_model):
        self.user.append(user_model.name)



@pytest.mark.asyncio
async def test_user_handler_creator(mock):
    #session = Session()
    session = mock()
    #session.commit = AsyncMock()
    user_schema = UserShema(name="ali", age=18)
    handler = service(session)
    user = await handler.user_create_handler(user_schema)
    #print(session.user)
    #assert session.user[0] == "ali"

    session.commit.assert_awaited_once()
    session.add.assert_called_once()



@pytest.mark.asyncio
async def test_invalid_age_does_not_reach_service():
    session = MagicMock(spec=AsyncSession)
    handler = service(session)

    with pytest.raises(ValidationError):
        body = UserShema(
            name="ali",
            age=17,
        )

        await handler.user_create_handler(body)

    session.add.assert_not_called()
    session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_from_db(mock):
    session = mock()
    handler = service(session)
    result = MagicMock()
    result.scalar_one_or_none.return_value = None

    session.execute.return_value = result
    with pytest.raises(ValueError):
        await handler.get_user_from_db(id="dummy", request="dummy")

    session.rollback.assert_called()


