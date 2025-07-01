from fastapi import APIRouter, Body
from pydantic import BaseModel
from datetime import date
from preprocessing.preprocesador import Preprocesador
from typing import Optional, List
import pandas as pd

router = APIRouter()
preprocesador = Preprocesador()

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
    required_skills: list[int] = []
    embedding: Optional[dict] = None

class filterMatchService(BaseModel):
    job_offer_id: int
    embedding: dict
    status: str
    stage: int

@router.post("/preprocess_job_offer", response_model=filterMatchService)
async def preprocess_job_offer(job_offer: Job_offer = Body(...)):
    df = pd.DataFrame([job_offer.dict()])
    embedding = preprocesador.get_embedding_offer(df)
    return filterMatchService(
        job_offer_id=job_offer.id,
        embedding={"vector": embedding[0].tolist()},
        status="processed",
        stage=1
    )

@router.post("/preprocess_all_job_offer")
async def preprocess_all_job_offer(job_offers: List[Job_offer] = Body(...)):
    df = pd.DataFrame([j.dict() for j in job_offers])
    embeddings = preprocesador.get_embeddings_alloffers(df)
    results = []
    for i, job_offer in enumerate(job_offers):
        results.append({
            "job_offer_id": job_offer.id,
            "embedding": {"vector": embeddings[i].tolist()},
            "status": "processed",
            "stage": 1
        })
    return results