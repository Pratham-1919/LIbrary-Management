from database.database import BaseManager
from datetime import datetime, timedelta
from models.Author import Authormanager
from models.Books import BookManager
from models.User import Managemember


class TransactionManager(BaseManager):
    def Give_book(self):
        try:
            member_id = int(input("Enter member ID: "))
        except ValueError:
            print("Invalid member ID.")
            return

        member_manager = Managemember()
        if not member_manager.get_details(member_id):
            print(f"Error: Member ID '{member_id}' not found in our records.")
            return

        title = input("Enter the book title you want: ")
        author_name = input("Provide the name of the author: ")
        try:
            qnt_to_borrow = int(input("Enter the quantity you want: "))
            if qnt_to_borrow <= 0:
                print("Quantity to borrow must be a positive number.")
                return
        except ValueError:
            print("Invalid quantity. Please enter a number.")
            return
        author_manager = Authormanager()
        book_manager = BookManager()

        author_data = author_manager.search_author(author_name)
    
        if not author_data:
            print(f"Error: Author '{author_name}' not found in our records.")
            return

        author_id = author_data[0]

        # 2. Get the Book ID using the Author ID and Title
        book_id = book_manager.get_book_id(title, author_id)

        if not book_id:
            print(f"Error: The book '{title}' by {author_name} is not in our library.")
            return

        # 3. Proceed to update stock (Decrease by the quantity borrowed)
        quantity_present = book_manager.get_book_quantity(book_id)

        if quantity_present is None:
            print("Could not retrieve book quantity. The book may not exist.")
            return
                    
        if quantity_present < qnt_to_borrow:
            print(f"Not enough copies available. Only {quantity_present} in stock.")
        else:
            new_quantity = quantity_present - qnt_to_borrow
            success = book_manager.update_book_quantity(book_id, new_quantity)
            if success:
                # Creating copy entries and transaction logs for the borrowed books
                issue_date = datetime.now()
                due_date = issue_date + timedelta(days=14)
                
                for _ in range(qnt_to_borrow):
                    # Register a copy of the book dynamically to issue
                    copy_query = "INSERT INTO book_copies (book_id, status) VALUES (%s, %s) RETURNING copy_id;"
                    copy_result = self._execute_query(copy_query, (book_id, False), fetchone=True, commit=True)
                    
                    if copy_result:
                        copy_id = copy_result[0]
                        trans_query = """
                            INSERT INTO transaction (copy_id, member_id, issue_date, due_date)
                            VALUES (%s, %s, %s, %s) RETURNING transaction_id;
                        """
                        self._execute_query(trans_query, (copy_id, member_id, issue_date, due_date), fetchone=True, commit=True)

                print(f"Success! {qnt_to_borrow} copies of '{title}' issued. Remaining stock: {new_quantity}.")
                self._logger.info(f"Transaction recorded: {qnt_to_borrow} copies of '{title}' issued to member {member_id}.")
            else:
                print("Failed to update inventory. Please check the logs.")

    def get_issued_books_for_member(self, member_id):
        """Retrieves all books currently issued to a specific member."""
        query = """
            SELECT b.title, a.name, t.issue_date, t.due_date
            FROM transaction t
            JOIN book_copies bc ON t.copy_id = bc.copy_id
            JOIN books b ON bc.book_id = b.book_id
            JOIN author a ON b.author_id = a.author_id
            WHERE t.member_id = %s AND t.return_date IS NULL
            ORDER BY t.due_date;
        """
        return self._execute_query(query, (member_id,), fetchall=True)

    def get_details(self, transaction_id):
        """Polymorphic method implementation for transaction."""
        query = "SELECT * FROM transaction WHERE transaction_id = %s;"
        return self._execute_query(query, (transaction_id,), fetchone=True)
