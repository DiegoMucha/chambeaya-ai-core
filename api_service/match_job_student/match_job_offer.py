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

@router.post("/best_job_offers")
async def best_job_offers(estudiante: Estudiante = Body(...)):
    df_jobs = pd.read_csv("datasets/puestos_test.csv")
    embedding_student = preprocesador.get_embedding_student(pd.DataFrame([estudiante.dict()]))
    embeddings_offers = preprocesador.get_embeddings_alloffers(df_jobs)
    scores, indexes = model.get_best_job_offers(embeddings_offers, embedding_student)
    results = []
    for rank, (idx, score) in enumerate(zip(indexes, scores), 1):
        job_offer_id = df_jobs.iloc[idx]["id_puesto"] if "id_puesto" in df_jobs.columns else df_jobs.iloc[idx]["id"]
        results.append({
            "job_offer_id": job_offer_id,
            "score": float(score),
            "rank": rank
        })
    return {"student_id": estudiante.id, "matches": results}