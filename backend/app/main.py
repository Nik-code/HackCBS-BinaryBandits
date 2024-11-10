# from fastapi import FastAPI
from .routes.user_routes import user_router
from .routes.doctor_routes import doctor_router
from .routes.appointment_routes import appointment_router
from .routes.hospital_routes import hospital_router
from .routes.symptom_routes import symptom_analysis_router
from .routes.lab_routes import lab_router
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.llm_services.disease_diagnosis_api import chat  # Importing the chatbot function

app = FastAPI()

allowed_origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # List of allowed origins
    allow_credentials=True,         # Allow cookies to be sent with requests
    allow_methods=["*"],            # Allow all HTTP methods (e.g., GET, POST)
    allow_headers=["*"],            # Allow all headers
)

# Include routers
app.include_router(user_router, prefix="/api/users", tags=["user"])
app.include_router(doctor_router, prefix="/api/doctors", tags=["doctor"])
app.include_router(appointment_router, prefix="/api/appointments", tags=["appointment"])
app.include_router(hospital_router, prefix="/api/hospitals", tags=["hospital"])
app.include_router(symptom_analysis_router, prefix="/api/symptoms", tags=["symptom_analysis"])
app.include_router(lab_router, prefix="/api/labs", tags=["lab"])
# Register other routes as needed

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the healthcare API"}

# Chatbot endpoint
@app.post("/api/chat")
async def chatbot_endpoint(request: Request):
    try:
        data = await request.json()
        user_message = data.get('message')
        thread_id = data.get('thread_id')
        reset = data.get('reset', False)

        if not user_message:
            raise HTTPException(status_code=400, detail="User message is required")

        response, new_thread_id = chat(user_message, thread_id, reset)
        return {"response": response, "thread_id": new_thread_id}
    except Exception as e:
        print("HERE")
        raise HTTPException(status_code=500, detail=str(e))

