import asyncio

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

    db.get_data()

asyncio.run(main())