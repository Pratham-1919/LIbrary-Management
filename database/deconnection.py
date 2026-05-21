from sqlalchemy import create_engine
from database.base import Base
from sqlalchemy.orm import sessionmaker

database_url = "postgresql+psycopg2://postgres:Pratham%4019@localhost:5432/Library"
engine = create_engine(database_url, echo=False)



try:
    with engine.connect() as connection:
        from sqlalchemy import text
        connection.execute(text("SELECT 0"))
        print("Connection Successful! Database responded.")
except Exception as e:
    print(f"Connection Failed: {e}")

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

from database.author import Author
from database.books import Books
from database.book_copies import BookCopies
from database.member import Member
from database.transaction import Transaction

# 4. Create your tables
print("Checking and creating tables...")
Base.metadata.create_all(engine)
print("Tables are ready!")