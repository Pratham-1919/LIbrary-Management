from datetime import datetime
from sqlalchemy import String, DateTime, Boolean, text
from sqlalchemy.orm import Mapped, mapped_column
from database.base import Base

class Member(Base):
    __tablename__ = "member"
    member_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(265), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    valid_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[bool] = mapped_column(Boolean, server_default=text("TRUE"), nullable=False)