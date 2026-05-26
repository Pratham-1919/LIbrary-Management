from fastapi import FastAPI,HTTPException

app = FastAPI()

@app.get("/User due date")
def User_due_date():
    return {"message : user due date is given as: "}