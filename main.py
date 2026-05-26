from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
import uvicorn

from models.User import Managemember
from models.Author import Authormanager
from models.Books import BookManager
from services.Transaction import TransactionManager
from database.deconnection import SessionLocal

app = FastAPI(title="Library Management System")


class MemberCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str

class BookCreate(BaseModel):
    title: str
    author_name: str
    price: float
    quantity: int = 5

class IssueBookRequest(BaseModel):
    member_id: int
    title: str
    author_name: str
    quantity: int = 1

class DeleteMember(BaseModel):
    member_id: int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- API Routes ---

@app.post("/members/", tags=["Member Management"])
def add_new_member(member: MemberCreate, db: Session = Depends(get_db)):
    manager = Managemember(db)
    manager.add_member(member.name, member.email, member.phone)
    return {"message": f"Member '{member.name}' added successfully."}

@app.post("/books/", tags=["Book Management"])
def add_new_book(book: BookCreate, db: Session = Depends(get_db)):
    author_manager = Authormanager(db)
    book_manager = BookManager(db)

    author_data = author_manager.search_author(book.author_name)
    if author_data:
        author_id = author_data.author_id
    else:
        author_id = author_manager.add_author(book.author_name)

    if author_id:
        book_id = book_manager.add_book(book.title, author_id, book.price, book.quantity)
        if book_id:
            return {"message": f"Book '{book.title}' added successfully.", "book_id": book_id}
            
    raise HTTPException(status_code=400, detail="Failed to add author or book.")

@app.get("/members/{member_id}/books", tags = ["Transaction Management"])
def check_book_status(member_id: int, db: Session = Depends(get_db)):
    member_manager = Managemember(db)
    if not member_manager.get_details(member_id):
        raise HTTPException(status_code=404, detail=f"Member ID '{member_id}' not found.")

    trans_manager = TransactionManager(db)
    issued_books = trans_manager.get_issued_books_for_member(member_id)

    if not issued_books:
        return {"message": f"No books are currently issued to member ID {member_id}.", "books": []}

    formatted_books = [
        {"title": b[0], "author": b[1], "issue_date": b[2], "due_date": b[3]} 
        for b in issued_books
    ]
    return {"member_id": member_id, "books": formatted_books}

@app.get("/transactions/issue", tags=["Book Management"])
def issue_book(req: IssueBookRequest, db: Session = Depends(get_db)):
    trans = TransactionManager(db)
    # We will call a newly refactored API method for transactions here
    success = trans.Give_book(req.member_id, req.title, req.author_name, req.quantity)
    if success:
        raise HTTPException(status_code=400, detail="Transaction failed. Check inventory or details.")
    return {"message": f"Successfully issued {req.quantity} copies of '{req.title}'."}

@app.get("/get_all_members/", tags=["Member Management"])
def Get_all_member(db : Session = Depends(get_db)):
    get_member = Managemember(db)
    member_details = get_member.get_all_members()
    return member_details

@app.delete("/delete_member/", tags = ["Member Management"])
def Delete_member(member = DeleteMember, db : Session = Depends(get_db)):
    deletemember = Managemember(db)
    deletedmember = deletemember.deactivate_member(member)
    return deletedmember




if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)