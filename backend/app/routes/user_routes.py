from fastapi import APIRouter, HTTPException, status, Depends, Request, Response
from datetime import datetime, timedelta
import bcrypt
from itsdangerous import URLSafeTimedSerializer
from app.models.user import User,  CreateUser
from app.database import database as db
from bson import ObjectId
import os

user_router = APIRouter()

# Secret key for signing session cookies
SECRET_KEY = os.getenv("SECRET_KEY", "secretkey")  # Secure with .env variable
serializer = URLSafeTimedSerializer(SECRET_KEY)

# Session expiration time (30 minutes)
SESSION_TIMEOUT = 1800

# # Password hashing function
# def hash_password(password: str) -> str:
#     salt = bcrypt.gensalt()
#     return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

# # Password verification function
# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

### Signup Route ###
# @user_router.post("/signup", response_model=User)
# async def signup(user: UserInCreate):
#     # await print(db["users"].find_one({"email": user.email}))
#     if await db["users"].find_one({"email": user.email}):
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
#     # Hash password
#     hashed_password = hash_password(user.password)
    
#     # Prepare user document
#     new_user = {
#         "email": user.email,
#         "passwordHash": hashed_password,
#         "createdAt": datetime.utcnow(),
#         "updatedAt": datetime.utcnow(),
#         "profile": user.profile,
#         "preferences": user.preferences
#     }
    
#     # Insert user into database
#     result = await db["users"].insert_one(new_user)
#     new_user["userId"] = result.inserteduserId
#     return User(**new_user)

# ### Login Route ###
# @user_router.post("/login")
# async def login(response: Response, email: str, password: str):
#     user = await db["users"].find_one({"email": email})
#     if not user or not verify_password(password, user["passwordHash"]):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
#     # Create session token and set as cookie
#     session_token = serializer.dumps(str(user["userId"]))
#     response.set_cookie(key="session_token", value=session_token, httponly=True, max_age=SESSION_TIMEOUT)
#     return {"message": "Login successful"}

# ### Middleware to Get Current User ###
# async def get_current_user(request: Request):
#     session_token = request.cookies.get("session_token")
#     if not session_token:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired or invalid")
    
#     try:
#         useruserId = serializer.loads(session_token, max_age=SESSION_TIMEOUT)
#     except Exception:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired or invalid")
    
#     user = await db["users"].find_one({"userId": ObjectId(useruserId)})
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
#     return User(**user)

# ### Protected Route to Get Current User ###
# @user_router.get("/users/me", response_model=User)
# async def read_users_me(current_user: User = Depends(get_current_user)):
#     return current_user

# ### Logout Route ###
# @user_router.post("/logout")
# async def logout(response: Response):
#     response.delete_cookie("session_token")
#     return {"message": "Logout successful"}

@user_router.post("/", response_model=User)
async def create_user(user: CreateUser):

    user_data = user.dict()
    user_data["createdAt"] = datetime.utcnow()
    user_data["updatedAt"] = datetime.utcnow()

    # Insert user into MongoDB
    result = await db["users"].insert_one(user_data)
    
    # Retrieve the user with _id from MongoDB
    created_user = await db["users"].find_one({"_id": result.inserted_id})
    print(created_user)
    
    return User(**created_user)



### Update User Route ###
@user_router.put("/{useruserId}", response_model=User)
async def update_user(useruserId: str, user: CreateUser):
    user.updatedAt = datetime.utcnow()
    user_dict = user.dict(by_alias=True, exclude_unset=True)
    result = await db["users"].update_one({"userId": ObjectId(useruserId)}, {"$set": user_dict})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = await db["users"].find_one({"userId": ObjectId(useruserId)})
    return User(**updated_user)

### Delete User Route ###
@user_router.delete("/{useruserId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(useruserId: str):
    result = await db["users"].delete_one({"userId": ObjectId(useruserId)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return None
