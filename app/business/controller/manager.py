
# from business import Factory, AccountFactory, AdminUserAccount, container, Role, UserRole

# class AdminUserAccountFactory(Factory):
#     @staticmethod
#     async def create(**kwargs):
#         user = kwargs["user"]
#         account = await AccountFactory.create(**kwargs)
#         user.create_account(account)
#         role = await container.get_factory(Role, role="admin", name="owner")
#         user_role = await container.get_factory(UserRole, role=role, user=kwargs["user"])
#         await account.add_user_admin(user_role)
#         admin_user_account = await container.get_factory(AdminUserAccount, role_user=user_role, account=account, user=kwargs["user"])
#         return admin_user_account