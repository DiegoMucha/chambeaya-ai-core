from fastapi import APIRouter, Body
from pydantic import BaseModel
from datetime import date
from preprocessing.preprocesador import Preprocesador
from models.KawsAIModel import KawsAIModel
from typing import List
import pandas as pd

router = APIRouter()
preprocesador = Preprocesador()
model = KawsAIModel()

class Job_offer(BaseModel):
    id: int
    title: str
    description: str
    required_hours: int
    approximated_salary: int
    duration: int
    start_date: date
    area_id: int
    experience_id: int
    modality: int
    required_skills: List[int] = []
    embedding: dict = None

class Estudiante(BaseModel):
    id: int
    name: str
    email: str
    career: str
    description: str
    weekly_availability: int
    preferred_modality: int
    experience_id: int
    date_of_birth: date
    skills: List[int] = []
    interests: List[int] = []
    embedding: dict = None

@router.post("/best_students")
async def best_students(job_offer: Job_offer = Body(...)):
    df_students = pd.read_csv("datasets/estudiantes_test.csv")
    embedding_offer = preprocesador.get_embedding_offer(pd.DataFrame([job_offer.dict()]))
    embeddings_students = preprocesador.get_embeddings_allstudents(df_students)
    scores, indexes = model.get_best_students(embeddings_students, embedding_offer)
    results = []
    for rank, (idx, score) in enumerate(zip(indexes, scores), 1):
        student_id = df_students.iloc[idx]["id_estudiante"] if "id_estudiante" in df_students.columns else df_students.iloc[idx]["id"]
        results.append({
            "student_id": student_id,
            "score": float(score),
            "rank": rank
        })
    return {"job_offer_id": job_offer.id, "matches": results}


