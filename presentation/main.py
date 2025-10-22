import asyncio

from data.model.user import User
from business import db

async def main():
    #ali = await Account.create("ali", "open")
    #await ali.add_wallet("wal")

    user = await User.create("ali", 23)
    #await user.add_role("admin")
    await user.create_account("namw", "ope")
    role = await Role.create("employee", "public")
    #userrole = await UserRole.create(user, role)

    db.get_data()

asyncio.run(main())