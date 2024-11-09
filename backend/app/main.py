# from fastapi import FastAPI
from app.routes.user_routes import user_router
from .routes.doctor_routes import doctor_router
from .routes.appointment_routes import appointment_router
from .routes.hospital_routes import hospital_router
from .routes.symptom_routes import symptom_analysis_router
from .routes.lab_routes import lab_router
from fastapi import FastAPI
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

from app.models.item2 import CreateItem2,GetItem2,Item2
from app.database import database as db
@app.post("/itemcreate")
async def add_item2(item:Item2):
    item2_data=item.dict()
    result=await db["item2"].insert_one(item2_data)
    created_item=await db["item2"].find_one({"_id": result.inserted_id})
    print(created_item)
    return GetItem2(**created_item)