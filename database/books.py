# books.py
from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, Numeric, Boolean, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship 
from database.author import Author
from database.base import Base

if TYPE_CHECKING:
    from database.book_copies import BookCopies

class Books(Base):
    __tablename__ = "books"

    book_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("author.author_id"), nullable=False
    )
    
    title: Mapped[str] = mapped_column(String(265), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[bool] = mapped_column(
        Boolean, server_default=text("TRUE"), nullable=False
    )

    author: Mapped["Author"] = relationship("Author", back_populates="books")   
    copies: Mapped[list["BookCopies"]] = relationship("BookCopies", back_populates="book", cascade="all, delete-orphan")