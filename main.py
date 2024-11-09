# from fastapi import FastAPI, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from datetime import timedelta
# from pydantic import BaseModel
# from auth import hash_password, verify_password, create_access_token, verify_token
# from fastapi.staticfiles import StaticFiles
# from fastapi.middleware.cors import CORSMiddleware
# app = FastAPI()
# allowed_origins = [
#     "http://localhost:5173"
# ]



# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=allowed_origins,  # List of allowed origins
#     allow_credentials=True,         # Allow cookies to be sent with requests
#     allow_methods=["*"],            # Allow all HTTP methods (e.g., GET, POST)
#     allow_headers=["*"],            # Allow all headers
# )

# # OAuth2PasswordBearer is a dependency that will retrieve and validate token
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# # In-memory "database"
# users_db = {
#     "user1": {
#         "username": "user1",
#         "password": "password123",
#     }
# }

# class User(BaseModel):
#     username: str

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# def authenticate_user(username: str, password: str):
#     user = users_db.get(username)
#     if user and password=="password123":
#         return User(username=username)
#     return None

# @app.post("/token", response_model=Token)
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(form_data.username, form_data.password)
#     print(user)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=30)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

# @app.get("/users/me", response_model=User)
# async def read_users_me(token: str = Depends(oauth2_scheme)):
#     payload = verify_token(token)
#     if payload is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid token",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return User(username=payload["sub"])








from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from pymongo import MongoClient
from bson import ObjectId
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB setup
client = MongoClient(os.getenv(""))
db = client[os.getenv("DB_NAME")]
users_collection = db["users"]

# FastAPI setup
app = FastAPI()

# Password hashing setup
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User model for Pydantic validation
class User(BaseModel):
    username: str
    password: str

class UserInDB(User):
    hashed_password: str

# Helper functions for password hashing
def hash_password(password: str) -> str:
    return bcrypt_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)

# Helper function for user retrieval
def get_user_by_username(username: str) -> Optional[dict]:
    return users_collection.find_one({"username": username})

# Register new user
@app.post("/register")
async def register_user(user: User):
    if get_user_by_username(user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = hash_password(user.password)
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_password
    
    users_collection.insert_one(user_dict)
    return {"message": "User created successfully"}

# Login user
@app.post("/login")
async def login_user(user: User):
    db_user = get_user_by_username(user.username)
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {"message": "Login successful"}

# Endpoint to get user details (for demonstration)
@app.get("/users/{username}")
async def get_user(username: str):
    user = get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"username": user["username"]}

