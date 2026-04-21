import logger
from models.User import Managemember
from models.Author import Authormanager
from models.Books import BookManager
from services.Transaction import TransactionManager

"""
        New user -> name,email,phone
        add book -> title, author name, quantity
        give book -> user -> name, book title, author name
        check book -> status -> False
"""


def add_new_member():
    """Handles the user input for adding a new member."""
    name = input("Enter member's name: ")
    email = input("Enter member's email: ")
    phone = input("Enter member's phone number: ")

    manager = Managemember()
    manager.add_member(name, email, phone)

def add_new_book():
    """Handles the user input for adding a new book."""
    title = input("Enter book title: ")
    author_name = input("Enter author's name: ")
    try:
        price = float(input("Enter book price: "))
        quantity_str = input("Enter book quantity (default is 5): ")
        quantity = int(quantity_str) if quantity_str else 5
    except ValueError:
        print("Invalid input for price or quantity. Please enter numbers.")
        return

    author_manager = Authormanager()
    book_manager = BookManager()

    # Check if author exists, if not, add them
    author_data = author_manager.search_author(author_name)
    if author_data:
        author_id = author_data[0]
    else:
        print(f"Author '{author_name}' not found. Adding as a new author.")
        author_id = author_manager.add_author(author_name)

    if author_id:
        book_id = book_manager.add_book(title, author_id, price, quantity)
        if book_id:
            print(f"Book '{title}' added successfully.")
        else:
            print("Failed to add book.")
    else:
        print("Could not find or create author. Book not added.")




def Check_book_status():
    """Handles checking the status of books issued to a member."""
    try:
        member_id = int(input("Enter member ID to check issued books: "))
    except ValueError:
        print("Invalid ID. Please enter a valid number.")
        return

    # Verify member exists
    member_manager = Managemember()
    if not member_manager.get_details(member_id):
        print(f"Error: Member ID '{member_id}' not found in our records.")
        return

    trans_manager = TransactionManager()
    issued_books = trans_manager.get_issued_books_for_member(member_id)

    if not issued_books:
        print(f"\nNo books are currently issued to member ID {member_id}.")
        return

    print(f"\n--- Books Issued to Member ID {member_id} ---")
    print(f"{'Title':<40} | {'Author':<25} | {'Issue Date':<20} | {'Due Date':<20}")
    print("-" * 115)
    for book in issued_books:
        title, author, issue_date, due_date = book
        issue_date_str = issue_date.strftime('%Y-%m-%d %H:%M')
        due_date_str = due_date.strftime('%Y-%m-%d %H:%M')
        print(f"{title:<40} | {author:<25} | {issue_date_str:<20} | {due_date_str:<20}")
    print("-" * 115)



def main():
    while True:
        print("\n--- Library Management System ---")
        print("1. Add a new member")
        print("2. Add a new book")
        print("3. Issue a book")
        print("4. Check given books.")
        print("5. Get user due date")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_new_member()
        elif choice == '2':
            add_new_book()
        elif choice == '3':
            trans = TransactionManager()
            trans.Give_book()
        elif choice == '4':
            Check_book_status()
        elif choice == '5':
            try:
                member_id = int(input("Enter member ID to check due date: "))
                auth = Managemember()
                due_date = auth.get_user_due_date(member_id)
                if due_date:
                    print(f"Due date for member {member_id}: {due_date}")
                else:
                    print(f"No record found for member ID {member_id}.")
            except ValueError:
                print("Invalid ID. Please enter a valid number.")
        else:
            print("Invalid Input")
            break
            


if __name__ == "__main__":
    main()