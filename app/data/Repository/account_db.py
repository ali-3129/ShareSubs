from .db import Db, Base
from infrastructure.bootstrap import container, account_observer
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey
from data.Repository.user_account_db import user_account


class AccountDb(Db):

    @staticmethod
    def get_branch():
        return "Account"

    @staticmethod
    def shema():
        return {
            "name": None,
            "status": None,
            "wallet": None,
            "users": [],
            "admins": [],
            "subscriptions": []
        }


account_db = container.get_singleton(AccountDb)
account_observer.attach(account_db)


class AccountModel(Base):
    from .user_db import UserModel
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column()
    users: Mapped[list["UserModel"]] = relationship("UserModel", secondary=user_account, back_populates="accounts")
