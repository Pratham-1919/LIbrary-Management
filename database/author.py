from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base

if TYPE_CHECKING:
    from database.books import Books

class Author(Base):     
    __tablename__ = "author"    

    author_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    # No need to import Books here! The string "Books" handles it.
    books: Mapped[list["Books"]] = relationship("Books", back_populates="author")