# app/main.py
from fastapi import FastAPI
from app.routers import items

app = FastAPI()

app.include_router(items.router, prefix="/items", tags=["items"])

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI MongoDB API!"}
