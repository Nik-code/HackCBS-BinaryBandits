# from fastapi import FastAPI
from app.routes.user_routes import user_router
from .routes.doctor_routes import doctor_router
from .routes.appointment_routes import appointment_router
from .routes.hospital_routes import hospital_router
from .routes.symptom_routes import symptom_analysis_router
from .routes.lab_routes import lab_router
# Import other routers as needed


from fastapi import FastAPI, HTTPException, Depends, status

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

from bson import ObjectId

def serialize_objectid(obj):
    """Helper function to convert ObjectId to string"""
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj

from app.models.item2 import CreateItem2,GetItem2,Item2
from app.database import database as db
@app.post("/itemcreate")
async def add_item2(item:Item2):
    item2_data=item.dict()
    result=await db["item2"].insert_one(item2_data)
    created_item=await db["item2"].find_one({"_id": result.inserted_id})
    print(created_item)
    # Serialize the user data, converting ObjectId to string
    # serialized_user = {key: serialize_objectid(value) for key, value in created_item.items()}

    # Return the serialized user as a GetUser model
    return GetItem2(**created_item)

# user_data = user.dict()
#     user_data["createdAt"] = datetime.utcnow()
#     user_data["updatedAt"] = datetime.utcnow()

#     # Insert user into MongoDB
#     result = db["users"].insert_one(user_data)
    
#     # Retrieve the user with _id from MongoDB
#     created_user = db["users"].find_one({"_id": result._id})
    
#     return GetUser(**created_user)