from .db import Db
from infrastructure.bootstrap import container, user_observer
from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from data.Repository.user_account_db import user_account


class UserDb(Db):

    @staticmethod
    def get_branch():
        return "User"

    @staticmethod
    def shema():
        return {
            "name": None,
            "age": None,
            "role": None,
            "roles": [],
            "accounts": [],
        }


user_db = container.get_singleton(UserDb)
user_observer.attach(user_db)


class UserModel(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=True)
    name: Mapped[str] = mapped_column()
    passhash: Mapped[str] = mapped_column(unique=True, nullable=True)
    role_name: Mapped[str] = mapped_column(ForeignKey("role.name", ondelete="CASCADE"), nullable=False, index=True)
    role: Mapped["RoleModel"] = relationship("RoleModel", back_populates="users")
    accounts: Mapped[list["AccountModel"]] = relationship("AccountModel", secondary=user_account, back_populates="users")
    tokens: Mapped[list["TokenModel"]] = relationship("TokenModel", back_populates="user")

