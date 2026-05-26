from database.database import BaseManager
from database.transaction import Transaction
from database.book_copies import BookCopies
from database.books import Books
from database.author import Author
from database.member import Member
from datetime import datetime, timedelta
from logger import logger


class TransactionManager(BaseManager):
    def Give_book(self,member_id, title, author_name, quantity):

        member = self.db.query(Member).get(member_id)
        if not member:
            print(f"Error: Member ID '{member_id}' not found in our records.")
            return

               
        try:
            if quantity <= 0:
                print("Quantity to borrow must be a positive number.")
                return
        except ValueError:
            print("Invalid quantity. Please enter a number.")
            return

        author = self.db.query(Author).filter(Author.name.ilike(author_name)).first()
        if not author:
            print(f"Error: Author '{author_name}' not found in our records.")
            return

        book = self.db.query(Books).filter(Books.title.ilike(title), Books.author_id==author.author_id).first()
        if not book:
            print(f"Error: The book '{title}' by {author_name} is not in our library.")
            return

        if book.quantity < quantity:
            print(f"Not enough copies available. Only {book.quantity} in stock.")
            return

        try:
            book.quantity -= quantity
            
            issue_date = datetime.now()
            due_date = issue_date + timedelta(days=14)
            
            for _ in range(quantity):
                new_copy = BookCopies(book_id=book.book_id, status=False)
                self.db.add(new_copy)
                self.db.flush()
                
                new_trans = Transaction(
                    copy_id=new_copy.copy_id, 
                    member_id=member_id, 
                    issue_date=issue_date, 
                    due_date=due_date
                )
                self.db.add(new_trans)
            
            self.db.commit()
            print(f"Success! {quantity} copies of '{title}' issued. Remaining stock: {book.quantity}.")
            logger.info(f"Transaction recorded: {quantity} copies of '{title}' issued to member {member_id}.")
        except Exception as e:
            self.db.rollback()
            print("Failed to update inventory. Please check the logs.")
            logger.error(f"Transaction failed: {e}")

    def issue_book_api(self, member_id: int, title: str, author_name: str, qnt_to_borrow: int = 1) -> bool:
        """API-friendly version of issuing a book (No CLI input)."""
        if qnt_to_borrow <= 0:
            logger.error("Quantity to borrow must be a positive number.")
            return False

        member = self.db.query(Member).get(member_id)
        if not member:
            logger.error(f"Error: Member ID '{member_id}' not found.")
            return False

        author = self.db.query(Author).filter(Author.name.ilike(author_name)).first()
        if not author:
            logger.error(f"Error: Author '{author_name}' not found.")
            return False

        book = self.db.query(Books).filter(Books.title.ilike(title), Books.author_id==author.author_id).first()
        if not book:
            logger.error(f"Error: The book '{title}' by {author_name} is not in our library.")
            return False

        if book.quantity < qnt_to_borrow:
            logger.error(f"Not enough copies. Only {book.quantity} in stock.")
            return False

        try:
            book.quantity -= qnt_to_borrow
            
            issue_date = datetime.now()
            due_date = issue_date + timedelta(days=14)
            
            for _ in range(qnt_to_borrow):
                new_copy = BookCopies(book_id=book.book_id, status=False)
                self.db.add(new_copy)
                self.db.flush()
                
                new_trans = Transaction(
                    copy_id=new_copy.copy_id, 
                    member_id=member_id, 
                    issue_date=issue_date, 
                    due_date=due_date
                )
                self.db.add(new_trans)
            
            self.db.commit()
            logger.info(f"Transaction recorded: {qnt_to_borrow} copies of '{title}' issued to member {member_id}.")
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Transaction failed: {e}")
            return False

    def get_issued_books_for_member(self, member_id):
        """Retrieves all books currently issued to a specific member."""
        return self.db.query(
            Books.title, 
            Author.name, 
            Transaction.issue_date, 
            Transaction.due_date
        ).join(BookCopies, BookCopies.copy_id == Transaction.copy_id)\
         .join(Books, Books.book_id == BookCopies.book_id)\
         .join(Author, Author.author_id == Books.author_id)\
         .filter(Transaction.member_id == member_id, Transaction.return_date == None)\
         .order_by(Transaction.due_date).all()

    def get_details(self, transaction_id):
        """Polymorphic method implementation for transaction."""
        return self.db.query(Transaction).get(transaction_id)
