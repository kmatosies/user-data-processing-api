from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from ..base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(24), primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
