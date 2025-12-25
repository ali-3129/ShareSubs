import asyncio
from asyncio import TaskGroup
from infrastructure.job import db_worker, producer
from asyncio import run, Queue
# from business import User
from business.model.factories import UserFactory
from data.Repository.db import db
from infrastructure.bootstrap import shot_down, metric, qeue
from fastapi import FastAPI, Request
from presentation.api.v1.routes.health import router as heals_router
from presentation.api.v1.routes.handler import router as user_router
from infrastructure.job import Task
import time
import uuid
from infrastructure.bootstrap import engine
from data.Repository.db import Base


def api():
    api = FastAPI()
    api.include_router(heals_router)
    api.include_router(user_router)
    return api


app = api()


@app.on_event("startup")
async def worker():
    app.state.workers = [
        asyncio.create_task(db_worker(qeue, "worker1")),
        asyncio.create_task(db_worker(qeue, "worker2"))
    ]


@app.middleware("http")
async def log(request: Request, call_next):
    req_id = request.headers.get("x_request_id")
    x_request_id = req_id or str(uuid.uuid4())
    request.state.x_request_id = x_request_id

    start = time.perf_counter()
    res = await call_next(request)
    duration = time.perf_counter() - start
    print(request, duration)
    res.headers["req_id"] = x_request_id
    return res


@app.on_event("shutdown")
async def off_worker():
    await qeue.join()
    shot_down.set()
    for worker in app.state.workers:
        await asyncio.gather(worker)
    db.get_data()


async def main():
    # ali = await Account.create("ali", "open")
    # await ali.add_wallet("wal")
    user = UserFactory(name="ali", age=23)
    account = await user.create()
    user1 = UserFactory(name="ali", age=23)
    await user1.create()
    # await worker()
    # await user.add_role("admin")
    # ''
    # role = await Role.create("employee", "public")
    # userrole = await UserRole.create(user, role)

    loop = asyncio.get_running_loop()

    db.get_data()
    await db.get_user_by_id(1)
    print(metric.get_all())

# asyncio.run(main())
