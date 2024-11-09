# # # app/main.py
# # from fastapi import FastAPI
# # from app.routers import items

# # app = FastAPI()

# # app.include_router(items.router, prefix="/items", tags=["items"])

# # @app.get("/")
# # async def root():
# #     return {"message": "Welcome to the FastAPI MongoDB API!"}


# # from fastapi import FastAPI, HTTPException, status, Body
# # from pydantic import BaseModel, Field, EmailStr
# # from typing import List, Optional
# # from datetime import datetime
# # from bson import ObjectId
# # from motor.motor_asyncio import AsyncIOMotorClient

# # from models.user import User
# # from models.doctor import Doctor
# # from models.hospital import Hospital
# # from models.symptom_analysis import SymptomAnalysis
# # from models.appointment import Appointment
# # from models.lab import Lab


# # # Sample User CRUD Routes
# # @app.post("/users/", response_model=User)
# # async def create_user(user: User):
# #     user.createdAt = datetime.utcnow()
# #     user.updatedAt = datetime.utcnow()
# #     user_dict = user.dict(by_alias=True)
# #     result = await db["users"].insert_one(user_dict)
# #     user_dict["_id"] = result.inserted_id
# #     return user_dict

# # @app.get("/users/{user_id}", response_model=User)
# # async def get_user(user_id: str):
# #     user = await db["users"].find_one({"_id": PyObjectId(user_id)})
# #     if not user:
# #         raise HTTPException(status_code=404, detail="User not found")
# #     return user

# # @app.put("/users/{user_id}", response_model=User)
# # async def update_user(user_id: str, user: User):
# #     user.updatedAt = datetime.utcnow()
# #     update_result = await db["users"].update_one({"_id": PyObjectId(user_id)}, {"$set": user.dict(by_alias=True)})
# #     if update_result.modified_count == 1:
# #         updated_user = await db["users"].find_one({"_id": PyObjectId(user_id)})
# #         return updated_user
# #     raise HTTPException(status_code=404, detail="User not found")

# # @app.delete("/users/{user_id}")
# # async def delete_user(user_id: str):
# #     delete_result = await db["users"].delete_one({"_id": PyObjectId(user_id)})
# #     if delete_result.deleted_count == 1:
# #         return {"message": "User deleted"}
# #     raise HTTPException(status_code=404, detail="User not found")

# # # SymptomAnalysis CRUD Routes
# # @app.post("/symptom_analysis/", response_model=SymptomAnalysis)
# # async def create_symptom_analysis(symptom_analysis: SymptomAnalysis):
# #     symptom_analysis.timestamp = datetime.utcnow()
# #     result = await db["symptom_analysis"].insert_one(symptom_analysis.dict(by_alias=True))
# #     return symptom_analysis

# # @app.get("/symptom_analysis/{chat_id}", response_model=SymptomAnalysis)
# # async def get_symptom_analysis(chat_id: str):
# #     symptom_analysis = await db["symptom_analysis"].find_one({"_id": PyObjectId(chat_id)})
# #     if not symptom_analysis:
# #         raise HTTPException(status_code=404, detail="Symptom Analysis not found")
# #     return symptom_analysis

# # # Similarly, create CRUD routes for Doctor, Hospital, Lab, Appointment, PatientHistory, Notification, etc.
# # # Each CRUD operation follows a similar pattern as shown above for User and SymptomAnalysis.

# # # Repeat similar CRUD routes for the remaining tables: Doctor, Hospital, Lab, Appointment, PatientHistory, etc.
# # # Structure each CRUD function in the same way as above to handle each data entity.


from fastapi import FastAPI
from app.routes.user_routes import user_router
from .routes.doctor_routes import doctor_router
from .routes.appointment_routes import appointment_router
from .routes.hospital_routes import hospital_router
from .routes.symptom_routes import symptom_analysis_router
from .routes.lab_routes import lab_router
# Import other routers as needed

app = FastAPI()

# Include routers
app.include_router(user_router, prefix="/api/users",tags=["user"])
app.include_router(doctor_router, prefix="/api/doctors",tags=["doctor"])
app.include_router(appointment_router, prefix="/api/appointments",tags=["appointment"])
app.include_router(hospital_router, prefix="/api/hospitals",tags=["hospital"])
app.include_router(symptom_analysis_router, prefix="/api/symptoms",tags=["symptom_analysis"])
app.include_router(lab_router, prefix="/api/labs",tags=["lab"])
# Register other routes as needed

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the healthcare API"}
