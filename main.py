import asyncio

#from business import User
from business.model.factories import UserFactory
from data.Repository.db import db

async def main():
    #ali = await Account.create("ali", "open")
    #await ali.add_wallet("wal")

    user = await UserFactory.create("ali", 23)
    #await user.add_role("admin")
    await user.create_account("namw", "ope")
    #role = await Role.create("employee", "public")
    #userrole = await UserRole.create(user, role)

    db.get_data()

asyncio.run(main())