from sqlalchemy import Integer, Boolean, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base 
from database.books import Books

class BookCopies(Base):
    __tablename__ = "book_copies"

    copy_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    book_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("books.book_id", ondelete="CASCADE"), nullable=False
    )
    

    status: Mapped[bool] = mapped_column(
        Boolean, server_default=text("TRUE"), nullable=False
    )

    book: Mapped["Books"] = relationship("Books", back_populates="copies")