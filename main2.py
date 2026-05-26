# from typing import Annotated
# from fastapi import Depends, FastAPI, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# app = FastAPI()

# # 1. Tells Swagger where the login form should submit its data
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# # 2. THE LOGIN ROUTE: This is what catches your username and password!
# @app.post("/token")
# async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#     # In a real app, you would check your database table here:
#     if form_data.username == "library_admin" and form_data.password == "secret123":
#         # If correct, send back a token string
#         return {"access_token": "super-secure-token-abc-123", "token_type": "bearer"}
    
#     # If incorrect, throw a real security error
#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED, 
#         detail="Incorrect username or password"
#     )

# # 3. THE SECURE ROUTE: Requires a token issued by the route above
# @app.get("/items/")
# async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"secret_data": "You are logged in!", "your_token": token}