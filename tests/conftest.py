import pytest, httpx
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
from app.infrastructure.bootstrap import ALGORITHM, SECRET_KEY
from app.infrastructure.bootstrap import DB_URL

from app.main import app
from app.presentation.api.v1.dependencies.sesstion import get_session
from app.infrastructure.security import create_token

@pytest_asyncio.fixture
async def client():
    async with LifespanManager(app):
        transport = httpx.ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac


@pytest_asyncio.fixture
async def login(client):
    r = await client.post("/users/signin/auth", json={
        "username": "aliaa44@example.com",
        "password": "123456789",
        "role_name": "string",
        "name": "ali225"
    })
    assert r.status_code == 200
    jwt = r.json()["access_token"]
    assert jwt != None
    print (jwt)
    return jwt


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


@pytest_asyncio.fixture
async def fake_session(test_session_factory):
    async with test_session_factory() as session:
            async def fake_commit():
                await session.flush()
            session.commit = fake_commit

            print("REAL OVERRIDE GET_SESSION CALLED")
            yield session

@pytest.fixture(autouse=True)
def get_session_override(fake_session):
    async def session_maker():
        yield fake_session
    app.dependency_overrides[get_session] = session_maker
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def create_fake_token(monkeypatch):

    def fake_create_token(*args, **kwargs):
        return create_token(
            sub=args[0],
            secret_key=args[1],
            expire_date=-1,
            algorithm=args[3],
        )
    monkeypatch.setattr(
        "app.presentation.api.v1.dependencies.user_handler.create_token",
        fake_create_token
    )
