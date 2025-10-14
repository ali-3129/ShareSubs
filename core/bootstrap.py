from core import AccountDb, Observer, Logger, UserDb, UserRollDb, RoleDb
db = AccountDb()
account_observer = Observer()
logger = Logger()
account_observer.attach(logger)
account_observer.attach(db)

user_logger = Logger()
user_db = UserDb()
user_observer = Observer()
user_observer.attach(user_db)
user_observer.attach(user_logger)

user_role_db = UserRollDb()
user_role_observer = Observer()
user_role_observer.attach(user_role_db)
user_role_logger = Logger()
user_role_observer.attach(user_role_logger)

role_logger = Logger()
role_db = RoleDb()
role_observer = Observer()
role_observer.attach(role_db)
role_observer.attach(role_logger)