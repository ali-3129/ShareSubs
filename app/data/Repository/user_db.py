from .db import Db
from infrastructure.bootstrap import container, user_observer
from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

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
    from .role_db import RoleModel
    __tablename__ = "users"
    id : Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    role_name: Mapped[str] = mapped_column(ForeignKey("role.name", ondelete="CASCADE"), nullable=False, index=True)
    role : Mapped[RoleModel] = relationship(back_populates="role")