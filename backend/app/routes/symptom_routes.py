from fastapi import APIRouter, HTTPException, status
from app.models.symptom_analysis import SymptomAnalysis,CreateSymptomAnalysis
from app.database import database as db
from bson import ObjectId
from datetime import datetime

symptom_analysis_router = APIRouter()

@symptom_analysis_router.post("/", response_model=SymptomAnalysis)
async def create_symptom_analysis(symptom_analysis: CreateSymptomAnalysis):
    symptom_analysis.timestamp = datetime.utcnow()
    symptom_analysis_dict = symptom_analysis.dict(by_alias=True)
    result = await db["symptom_analysis"].insert_one(symptom_analysis_dict)
    symptom_analysis_dict["_id"] = result.inserted_id
    return symptom_analysis_dict

@symptom_analysis_router.get("/{chat_id}", response_model=SymptomAnalysis)
async def get_symptom_analysis(chat_id: str):
    symptom_analysis = await db["symptom_analysis"].find_one({"_id": ObjectId(chat_id)})
    if symptom_analysis is None:
        raise HTTPException(status_code=404, detail="Symptom analysis not found")
    return SymptomAnalysis(**symptom_analysis)

@symptom_analysis_router.put("/{chat_id}", response_model=SymptomAnalysis)
async def update_symptom_analysis(chat_id: str, symptom_analysis: CreateSymptomAnalysis):
    symptom_analysis.timestamp = datetime.utcnow()
    symptom_analysis_dict = symptom_analysis.dict(by_alias=True, exclude_unset=True)
    result = await db["symptom_analysis"].update_one({"_id": ObjectId(chat_id)}, {"$set": symptom_analysis_dict})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Symptom analysis not found")
    updated_symptom_analysis =await  db["symptom_analysis"].find_one({"_id": ObjectId(chat_id)})
    return SymptomAnalysis(**updated_symptom_analysis)

@symptom_analysis_router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_symptom_analysis(chat_id: str):
    result = await db["symptom_analysis"].delete_one({"_id": ObjectId(chat_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Symptom analysis not found")
    return None
