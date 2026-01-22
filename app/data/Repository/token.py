
from sqlalchemy.orm import Mapped, mapped_column, Relationship, relationship
from sqlalchemy import ForeignKey, String, DateTime, func
from app.data.Repository.db import Base
import datetime


class TokenModel(Base):
    __tablename__ = "tokens"
    token_id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    user_name: Mapped[str] = mapped_column(ForeignKey("users.name", ondelete="CASCADE"), index=True)
    token_hash: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="tokens")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[datetime or None] = mapped_column(DateTime(timezone=True), nullable=True)
