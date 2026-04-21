from database.database import BaseManager

class BookManager(BaseManager):
    def add_book(self, title, author_id, price, quantity=5):
        """
        Inserts a new book into the library.
        Note: author_id must come from the author table.
        """
        query = """
            INSERT INTO books (title, author_id, price, quantity, status)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING book_id;
        """
        result = self._execute_query(query, (title, author_id, price, quantity, True), fetchone=True, commit=True)
        if result:
            self._logger.info(f"Book '{title}' added successfully with ID: {result[0]}")
            return result[0]
        return None

    def get_all_books_with_authors(self):
        """
        Retrieves a complete list of books showing the Author's Name 
        instead of just the ID using an INNER JOIN.
        """
        query = """
            SELECT b.book_id, b.title, a.name, b.price, b.quantity
            FROM books b
            INNER JOIN author a ON b.author_id = a.author_id
            ORDER BY b.book_id DESC;
        """
        return self._execute_query(query, fetchall=True) or []

    def update_book_quantity(self, book_id, new_quantity):
        """Updates the stock level for a specific book."""
        query = "UPDATE books SET quantity = %s WHERE book_id = %s;"
        return self._execute_query(query, (new_quantity, book_id), commit=True) is not None
        
    def get_book_id(self, title, author_id):
        """Fetches the book_id based on title and author_id."""
        query = "SELECT book_id FROM books WHERE title = %s AND author_id = %s;"
        result = self._execute_query(query, (title, author_id), fetchone=True)
        return result[0] if result else None
        
    def get_book_quantity(self,book_id):
        """To get the total quantity of the book"""
        query = "SELECT quantity FROM books WHERE book_id = %s"
        result = self._execute_query(query, (book_id,), fetchone=True)
        return result[0] if result else None
        
    def update_book_status(self, book_id, status):
        """To update the book status"""
        query = "UPDATE books SET status = %s WHERE book_id = %s"
        return self._execute_query(query, (status, book_id), commit=True) is not None

    def get_details(self, book_id):
        """Polymorphic method implementation for book."""
        query = "SELECT * FROM books WHERE book_id = %s;"
        return self._execute_query(query, (book_id,), fetchone=True)