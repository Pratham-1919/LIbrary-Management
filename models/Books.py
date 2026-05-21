from database.database import BaseManager
from database.books import Books
from database.author import Author
from database.deconnection import session
from logger import  logger

class BookManager(BaseManager):
    def add_book(self, book_title, book_author_id, book_price, book_quantity=5):
        with session as Session:
            try:
                """
                Inserts a new book into the library.
                Note: author_id must come from the author table.
                """
                new_book = Books(author_id = book_author_id, title = book_title, price = book_price, quantity = book_quantity)
                Session.add(new_book) 
                Session.commit()
                logger.info("Book added successfully.") 
                return new_book.book_id
            except Exception as e:
                Session.rollback()
                logger.error("Failed to add book: ")
                return    


    def get_all_books_with_authors(self):
        """
        Retrieves a complete list of books showing the Author's Name 
        instead of just the ID using an INNER JOIN.
        """
        with session as Session:
            return Session.query(
                Books.book_id, Books.title, Author.name, Books.price, Books.quantity
            ).join(Author, Books.author_id == Author.author_id).order_by(Books.book_id.desc()).all()

    def update_book_quantity(self, book_id, new_quantity):
        """Updates the stock level for a specific book."""
        with session as Session:
            try:
                book = Session.query(Books).get(book_id)
                if book:
                    book.quantity = new_quantity
                    Session.commit()
                    return True
                return False
            except Exception as e:
                Session.rollback()
                logger.error(f"Failed to update book quantity: {e}")
                return False
        
    def get_book_id(self, title, author_id):
        """Fetches the book_id based on title and author_id."""
        with session as Session:
            book = Session.query(Books).filter(Books.title.ilike(title), Books.author_id==author_id).first()
            return book.book_id if book else None
        
    def get_book_quantity(self,book_id):
        """To get the total quantity of the book"""
        with session as Session:
            book = Session.query(Books).get(book_id)
            return book.quantity if book else None
        
    def update_book_status(self, book_id, status):
        """To update the book status"""
        with session as Session:
            try:
                book = Session.query(Books).get(book_id)
                if book:
                    book.status = status
                    Session.commit()
                    return True
                return False
            except Exception as e:
                Session.rollback()
                logger.error(f"Failed to update book status: {e}")
                return False

    def get_details(self, book_id):
        """Polymorphic method implementation for book."""
        with session as Session:
            return Session.query(Books).get(book_id)