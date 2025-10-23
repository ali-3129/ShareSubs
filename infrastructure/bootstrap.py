from .common import Logger, RoleObserver, AccountObserver, UserRoleObserver, UserObserver
from .container import Container

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