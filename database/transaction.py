from database.base import Base
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship 
from sqlalchemy import  Integer, ForeignKey, DateTime
from database.book_copies import BookCopies
from database.member import Member



        # CREATE TABLE IF NOT EXISTS transaction(
        #     transaction_id SERIAL PRIMARY KEY,
        #     copy_id INT NOT NULL,
        #     member_id INT NOT NULL,
        #     issue_date TIMESTAMP,
        #     due_date TIMESTAMP,
        #     return_date TIMESTAMP,
        #     FOREIGN KEY (copy_id) REFERENCES book_copies (copy_id),
        #     FOREIGN KEY (member_id) REFERENCES member (member_id)
        # );
if TYPE_CHECKING:
    from database.book_copies import BookCopies
    from database.member import Member

class Transaction(Base):
    __tablename__ = "transaction"

    transaction_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    copy_id: Mapped[int] = mapped_column(Integer, ForeignKey("book_copies.copy_id"), nullable=False)
    member_id: Mapped[int] = mapped_column(Integer, ForeignKey("member.member_id"), nullable=False)
    issue_date: Mapped[DateTime | None] = mapped_column(DateTime, nullable = True) 
    due_date: Mapped[DateTime | None] = mapped_column(DateTime, nullable = True) 
    return_date: Mapped[DateTime | None] = mapped_column(DateTime, nullable = True) 
    book_copy: Mapped["BookCopies"] = relationship("BookCopies")
    member: Mapped["Member"] = relationship("Member")
