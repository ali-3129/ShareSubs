import asyncio
from asyncio import TaskGroup
from infrastructure.job import db_worker, producer
from asyncio import run, Queue
#from business import User
from business.model.factories import UserFactory
from data.Repository.db import db
from infrastructure.bootstrap import shot_down, metric
from fastapi import FastAPI
from presentation.api.v1.routes.health import router as heals_router
from presentation.api.v1.routes.handler import router as user_router

def api():
    api = FastAPI()
    api.include_router(heals_router)
    api.include_router(user_router)
    return api


app = api()

async def main():

    #ali = await Account.create("ali", "open")
    #await ali.add_wallet("wal")
    user = UserFactory(name="ali", age=23)
    account = await user.create()
    #await user.add_role("admin")
    # ''
    #role = await Role.create("employee", "public")
    #userrole = await UserRole.create(user, role)

    loop = asyncio.get_running_loop()
    qeue = Queue()
    async with TaskGroup() as tg:
        try:
            workers = [
                tg.create_task(db_worker(qeue, "worker1")),
                tg.create_task(db_worker(qeue, "worker2"))
            ]
        except:pass

        await producer(qeue)
        await qeue.join()
        shot_down.set()
        for worker in workers:
            await asyncio.gather(worker)


    db.get_data()
    print(metric.get_all())


#asyncio.run(main())
