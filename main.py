from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from pydantic import BaseModel
from auth import hash_password, verify_password, create_access_token, verify_token
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
allowed_origins = [
    "http://localhost:5173"
]



app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # List of allowed origins
    allow_credentials=True,         # Allow cookies to be sent with requests
    allow_methods=["*"],            # Allow all HTTP methods (e.g., GET, POST)
    allow_headers=["*"],            # Allow all headers
)

# OAuth2PasswordBearer is a dependency that will retrieve and validate token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# In-memory "database"
users_db = {
    "user1": {
        "username": "user1",
        "password": "password123",
    }
}

class User(BaseModel):
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str

def authenticate_user(username: str, password: str):
    user = users_db.get(username)
    if user and password=="password123":
        return User(username=username)
    return None

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return User(username=payload["sub"])









