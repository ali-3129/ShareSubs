import asyncio
from infrastructure.job import db_worker, producer
from asyncio import run, Queue
#from business import User
from business.model.factories import UserFactory
from data.Repository.db import db

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
    worker.cancel()
    await asyncio.gather(worker)
    db.get_data()


asyncio.run(main())