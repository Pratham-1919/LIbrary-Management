from database.database import BaseManager
from database.deconnection import session
from database.transaction import Transaction
from database.book_copies import BookCopies
from database.books import Books
from database.author import Author
from database.member import Member
from datetime import datetime, timedelta
from logger import logger


class TransactionManager(BaseManager):
    def Give_book(self):
        try:
            member_id = int(input("Enter member ID: "))
        except ValueError:
            print("Invalid member ID.")
            return

        with session as Session:
            member = Session.query(Member).get(member_id)
            if not member:
                print(f"Error: Member ID '{member_id}' not found in our records.")
                return

            title = input("Enter the book title you want: ").strip()
            author_name = input("Provide the name of the author: ").strip()
            
            try:
                qnt_to_borrow = int(input("Enter the quantity you want: "))
                if qnt_to_borrow <= 0:
                    print("Quantity to borrow must be a positive number.")
                    return
            except ValueError:
                print("Invalid quantity. Please enter a number.")
                return

            author = Session.query(Author).filter(Author.name.ilike(author_name)).first()
            if not author:
                print(f"Error: Author '{author_name}' not found in our records.")
                return

            book = Session.query(Books).filter(Books.title.ilike(title), Books.author_id==author.author_id).first()
            if not book:
                print(f"Error: The book '{title}' by {author_name} is not in our library.")
                return

            if book.quantity < qnt_to_borrow:
                print(f"Not enough copies available. Only {book.quantity} in stock.")
                return

            try:
                book.quantity -= qnt_to_borrow
                
                issue_date = datetime.now()
                due_date = issue_date + timedelta(days=14)
                
                for _ in range(qnt_to_borrow):
                    new_copy = BookCopies(book_id=book.book_id, status=False)
                    Session.add(new_copy)
                    Session.flush()
                    
                    new_trans = Transaction(
                        copy_id=new_copy.copy_id, 
                        member_id=member_id, 
                        issue_date=issue_date, 
                        due_date=due_date
                    )
                    Session.add(new_trans)
                
                Session.commit()
                print(f"Success! {qnt_to_borrow} copies of '{title}' issued. Remaining stock: {book.quantity}.")
                logger.info(f"Transaction recorded: {qnt_to_borrow} copies of '{title}' issued to member {member_id}.")
            except Exception as e:
                Session.rollback()
                print("Failed to update inventory. Please check the logs.")
                logger.error(f"Transaction failed: {e}")

    def get_issued_books_for_member(self, member_id):
        """Retrieves all books currently issued to a specific member."""
        with session as Session:
            return Session.query(
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
        with session as Session:
            return Session.query(Transaction).get(transaction_id)
