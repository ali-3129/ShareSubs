import asyncio
from infrastructure.job import db_worker, producer
from asyncio import run, Queue
#from business import User
from business.model.factories import UserFactory
from data.Repository.db import db
from infrastructure.bootstrap import SENTINEL

async def main():


    #ali = await Account.create("ali", "open")
    #await ali.add_wallet("wal")
    user = UserFactory(name="ali", age=23)
    account = await user.create()
    #await user.add_role("admin")
    # ''
    #role = await Role.create("employee", "public")
    #userrole = await UserRole.create(user, role)


    qeue = Queue()
    worker = asyncio.create_task(db_worker(qeue, "worker1"))
    await producer(qeue)
    await qeue.join()
    #await qeue.put(SENTINEL)
    worker.cancel()
    try:
        await asyncio.gather(worker)
    except:
        pass

    db.get_data()


asyncio.run(main())