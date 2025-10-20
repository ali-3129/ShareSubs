from core.common import AccountDb, Logger, UserDb, UserRollDb, RoleDb, AccountObserver, UserObserver, UserRoleObserver, RoleObserver
from container import Container

container = Container()
logger = container.get_singleton(Logger)

db = container.get_singleton(AccountDb)
account_observer = container.get_scoped(AccountObserver)
account_observer.attach(logger)
account_observer.attach(db)

user_db = container.get_singleton(UserDb)
user_observer = container.get_scoped(UserObserver)
user_observer.attach(user_db)
user_observer.attach(logger)

user_role_db = container.get_singleton(UserRollDb)
user_role_observer = container.get_scoped(UserRoleObserver)
user_role_observer.attach(user_role_db)
user_role_observer.attach(logger)

role_db = container.get_singleton(RoleDb)
role_observer = container.get_scoped(RoleObserver)
role_observer.attach(role_db)
role_observer.attach(logger)