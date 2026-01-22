from typing import AsyncGenerator
from app.infrastructure.bootstrap import session_maker
from sqlalchemy.ext.asyncio import AsyncSession


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session