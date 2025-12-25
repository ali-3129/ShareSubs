from pathlib import Path
from .common import Logger, RoleObserver, AccountObserver, UserRoleObserver, UserObserver, Metric
from .container import Container
import asyncio
from asyncio import Queue
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_URL = "sqlite+aiosqlite:///C:/Users/ASUS/Desktop/ShareSubs/app/app.db"

engine = create_async_engine(DB_URL)

session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


container = Container()
logger = container.get_singleton(Logger)

account_observer = container.get_scoped(AccountObserver)
account_observer.attach(logger)

user_observer = container.get_scoped(UserObserver)
user_observer.attach(logger)

user_role_observer = container.get_scoped(UserRoleObserver)
user_role_observer.attach(logger)

role_observer = container.get_scoped(RoleObserver)
role_observer.attach(logger)
sem = asyncio.Semaphore(5)
shot_down = asyncio.Event()
metric = Metric()
qeue = Queue()