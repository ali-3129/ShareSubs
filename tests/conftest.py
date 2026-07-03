import pytest, httpx
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
from app.infrastructure.bootstrap import DB_URL

from app.main import app
from app.presentation.api.v1.dependencies.sesstion import get_session

@pytest_asyncio.fixture
async def client():
    async with LifespanManager(app):
        transport = httpx.ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac


@pytest_asyncio.fixture
async def login(client):
    r = await client.post("/users/singin/auth", json={
        "username": "aliaaaaaaa@aaexample.com",
        "password": "123456789",
        "role_name": "string",
        "name": "ali225"
    })
    assert r.status_code == 200
    jwt = r.json()["access_token"]
    assert jwt != None
    print (jwt)


@pytest_asyncio.fixture
async def test_session_factory():
    engine = create_async_engine (
        DB_URL,
        echo=False
    )
    conection = await engine.connect()
    transaction = await conection.begin()
    session_factory = async_sessionmaker (
        bind=conection,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        join_transaction_mode="create_savepoint"
    )
    
    try:
        yield session_factory
    finally:
        print("roll back")
        await transaction.rollback()
        await conection.close()
        await engine.dispose()


@pytest.fixture(autouse=True)
def get_session_override(test_session_factory):
    async def session_manker():
        async with test_session_factory() as session:
            async def fake_commit():
                await session.flush()
            session.commit = fake_commit

            print("REAL OVERRIDE GET_SESSION CALLED")
            yield session
    app.dependency_overrides[get_session] = session_manker
    print("TEST GET_SESSION USED")
    yield
    app.dependency_overrides.clear()